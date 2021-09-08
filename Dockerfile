FROM alpine:3.14

WORKDIR /app

RUN apk update \
    && apk add python3 \
    && apk add py3-pip py3-gunicorn \
    && apk add --virtual .build-deps alpine-sdk python3-dev libffi-dev \
    && apk add --virtual .python-deps py3-flask \
    && pip3 install --upgrade pip \
    && pip3 install --ignore-installed pipenv

COPY Pipfile /app/Pipfile
COPY Pipfile.lock /app/Pipfile.lock

RUN pipenv install --system --dev --deploy \
    && apk del .build-deps \
    && rm -rf /var/cache/apk/*

COPY . /app

EXPOSE 5300
