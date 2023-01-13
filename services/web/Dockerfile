FROM python:3.9-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN apk add --no-cache netcat-openbsd

COPY . /usr/src/app/