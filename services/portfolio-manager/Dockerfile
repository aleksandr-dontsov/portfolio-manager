FROM python:3.8-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./Pipfile ./Pipfile.lock /usr/src/app/

RUN pip install --upgrade pip && \
    pip install pipenv

# --system Installs dependencies in Pipfile system-wide
# --deploy Abort if Pipfile.lock is out-of-date
RUN pipenv install --system --deploy
RUN apk add --no-cache netcat-openbsd

COPY . /usr/src/app/