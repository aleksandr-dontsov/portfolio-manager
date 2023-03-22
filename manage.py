import os
import signal
import subprocess

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


@click.group()
def cli():
    pass


@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("subcommand", nargs=-1, type=click.Path())
def flask(subcommand):
    cmdline = ["flask"] + list(subcommand)
    try:
        p = subprocess.Popen(cmdline)
        p.wait()
    except KeyboardInterrupt:
        p.send_signal(signal.SIGINT)
        p.wait()


@cli.command()
def create_initial_db():
    create_db(os.getenv("APPLICATION_DB"))


if __name__ == "__main__":
    cli()
