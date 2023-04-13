# Portfolio Manager

`Portfolio Manager` is a web service that manages financial portfolios.

# Table of Contents

1. [Prerequisites](#prerequisites)
2. [Setup the project](#setup-the-project)
3. [Run service in Dev](#run-service-in-dev)
4. [Run service in Prod](#run-service-in-prod)
5. [Testing](#testing)
6. [API](#api)
7. [Contact](#contact)

## Prerequisites

- Required software: Python, Docker, VSCode.
- External services: PostgreSQL, Nginx, Gunicorn.
- Additional tools, libraries: pipenv.

## Setup the project

To setup the working environment:

1. Clone the repository.
2. Install dependencies using `pipenv`.
    > pipenv install --dev
3. Spawn a shell within the virtualenv using `pipenv`.
    > pipenv shell
4. Open the project in VSCode.
5. Select interpreter from the virualenv created in the step 3.

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

## API

API can be found by the url `http://localhost:<port>/api/ui/` where <port> is `5000` for dev and `1337` for prod environments. There you also can try it out.

## Contact

- Maintainer: Aleksandr Dontsov
- Email: dontsov.aleksander@gmail.com
