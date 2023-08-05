# Portfolio Manager

`Portfolio Manager` is a web service that manages financial portfolios.

# Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project structure](#project-structure)
3. [Setup the project](#setup-the-project)
4. [Run service in Dev](#run-service-in-dev)
5. [Run service in Prod](#run-service-in-prod)
6. [Testing](#testing)
7. [API](#api)
8. [Contact](#contact)

## Prerequisites

- Required software: Python, Docker.
- External services: PostgreSQL, Nginx, Gunicorn.
- Additional tools, libraries: pipenv.

## Project structure

- `app` folder contains the application code
- `config` folder includes configuration files for different stages
- `docker` folder contains docker-related files to run services in Docker
- `migrations` folder contains [alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html#the-migration-environment) database migration files
- `nginx` folder contains [nginx](https://www.nginx.com/) files to run it in Docker. nginx is used in `prod` environment as a reverse proxy server alongside with [gunicorn](https://gunicorn.org/)
- `tests` folder contains functional and unit tests for the project
- `manage.py` script contains functions for running the service in Docker
- `Pipfile` and `Pipfile.lock` files contain project dependencies and used by `pipenv`
- `swagger.yml` file describes the API of the service
- `wsgi.py` script is the main entry point of the service and is run by the web server.

## Setup the project

To setup the working environment:

1. Clone the repository.
2. Install dependencies using `pipenv`.
    > pipenv install --dev
3. Spawn a shell within the virtualenv using `pipenv`.
    > pipenv shell
4. Open the project in your favourite IDE.
5. User the interpreter from the virualenv created in the step 3.

## Run service in Dev

For the following commands you need to activate a virtualenv first with `pipenv`.

To run the service in dev environment:

1. Build dev Docker images.
    > ./manage.py compose dev build --pull
2. Run dev Docker containers.
    > ./manage.py compose dev up -dV

For the first time launch setup the db:

1. Create db.
    > ./manage.py compose dev run web ./manage.py create-initial-db
2. Migrate db to the initial state.
    > ./manage.py compose dev run web flask db upgrade

To stop the service:
1. Stop dev Docker containers
    > ./manage.py compose dev down

The service should be accessible by the url `http://localhost:5000`

## Run service in Prod

Instructions for **Prod** environment are similar to [Dev](#run-service-in-dev) except that `prod` stage must be used instead of `dev` as the first argument after `compose` command.

Example: `./manage.py compose prod build --pull`

The service should be accessible by the url `http://localhost:1337`

## Testing

You need to activate a virtualenv and execute the following command:

1. Run tests
    > ./manage.py test

It's also possible to pass multiple test expression parameters after the `test` command.

Example: `./manage.py test test_duplicate_portfolio_create`

## API

API can be found by the url `http://localhost:<port>/api/ui/` where <port> is `5000` for dev and `1337` for prod environments. There you also can try it out.

## Contact

- Maintainer: Aleksandr Dontsov
- Email: dontsov.aleksander@gmail.com
