#!/usr/bin/env python

import os
import subprocess
import signal
import time
import pathlib

import click
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def run_sql(statements):
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOSTNAME"),
        port=os.getenv("POSTGRES_PORT"),
    )
    # To ensure that each SQL statement we execute will be
    # immediately committed to the database
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    for statement in statements:
        cursor.execute(statement)

    cursor.close()
    conn.close()


def create_db(database_name):
    try:
        run_sql([f"CREATE DATABASE {database_name}"])
    except psycopg2.errors.DuplicateDatabase:
        print(f"The database {database_name} already exists")


def docker_compose_cmdline(stage):
    projectdir = pathlib.Path(__file__).parent.resolve()
    dockerdir = os.path.join(projectdir, "docker")
    docker_compose_file = os.path.join(dockerdir, f"docker-compose.{stage}.yml")

    if not os.path.isfile(docker_compose_file):
        raise ValueError(f"The file {docker_compose_file} does not exist")

    return ["docker-compose", "-p", stage, "-f", docker_compose_file]


@click.group()
def cli():
    pass


# context_settings - a dictionary with defaults passed to the context
# ignore_unknown_options - forwards unknown options rather than triggering a parsing error
# argument - similar to options but are positional
# nargs - specifies a number of arguments is accepted. -1 accepts an unlimited number of args
# Path - type is similar to File, but returns the filename instead of an open file
@cli.command(context_settings=dict(ignore_unknown_options=True))
@click.argument("stage", nargs=1, type=click.Path())
@click.argument("subcommand", nargs=-1, type=click.Path())
def compose(stage, subcommand):
    cmdline = docker_compose_cmdline(stage) + list(subcommand)

    try:
        p = subprocess.Popen(cmdline)
        p.wait()
    except KeyboardInterrupt:
        p.send_signal(signal.SIGINT)
        p.wait()


@cli.command()
@click.argument("tests", nargs=-1)
def test(tests):
    cmdline = docker_compose_cmdline("test") + ["up", "-d"]
    subprocess.call(cmdline)

    cmdline = docker_compose_cmdline("test") + ["logs", "db"]
    logs = subprocess.check_output(cmdline).decode("utf-8")
    while "ready to accept connections" not in logs:
        time.sleep(0.1)
        logs = subprocess.check_output(cmdline).decode("utf-8")

    # -s - do not capture output
    # -vv - increases verbosity adding test function names
    # --cov - path or package name to measure during execution
    # --cov-report - coverage report type. term-missing shows the lines which are not covered
    cmdline = [
        "python",
        "-m",
        "pytest",
        "-svv",
        "--cov=app",
        "--cov-report=term-missing",
        "tests",
    ]
    if tests:
        cmdline.extend(["-k"])
        cmdline.extend(tests)

    subprocess.call(cmdline)

    cmdline = docker_compose_cmdline("test") + ["down"]
    subprocess.call(cmdline)


@cli.command()
def create_initial_db():
    create_db(os.getenv("APPLICATION_DB"))


if __name__ == "__main__":
    cli()
