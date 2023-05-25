#!/bin/sh

if [ "$DATABASE_DIALECT" = "postgres" ]
then
    echo "Waiting for postgres..."
    while ! nc -z $POSTGRES_HOSTNAME $POSTGRES_PORT; do
        sleep 0.1
    done
    echo "PostgresSQL started"
fi

exec "$@"
