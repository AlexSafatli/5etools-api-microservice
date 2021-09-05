FROM alpine:3.9

WORKDIR /app

RUN apk update \
    && apk add python3 \
    && apk add --virtual .build-deps alpine-sdk python3-dev libffi-dev \
    && apk add --virtual .python-deps py3-flask \
    && pip3 install --upgrade pip \
    && pip3 install pipenv

COPY Pipfile /app/Pipfile

RUN pipenv install --system --dev --deploy \
    && apk del .build-deps \
    && rm -rf /var/cache/apk/*

COPY . /app

EXPOSE 5300
