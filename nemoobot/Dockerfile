# TODO use alpine image
FROM python:3.9.0-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add gcc musl-dev python3-dev libffi-dev openssl-dev

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

COPY ./entrypoint.sh .

ENTRYPOINT ["sh", "/usr/src/nemoobot/entrypoint.sh"]