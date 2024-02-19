FROM python:3.12-alpine

WORKDIR /richPanel

RUN apk --no-cache update && \
    apk add --no-cache gcc git python3-dev musl-dev libffi-dev openssl-dev build-base

ENV PYTHONUNBUFFERED 0

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
# RUN apk add python3-psycopg2
RUN pip install psycopg2-binary

EXPOSE 8000 5050 
