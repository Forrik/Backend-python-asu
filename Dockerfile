FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1
ENV TZ=Europe/Moscow

RUN apt-get update && apt-get install -y libpq-dev make build-essential \
    linux-headers-generic libpcre3-dev python3-dev libjpeg-dev zlib1g-dev \
    tzdata libffi-dev libssl-dev libc-dev curl

WORKDIR /opt/drf_project


COPY Pipfile* ./

RUN pip install --upgrade pip pipenv wheel
RUN pipenv install --system -d

COPY ./src/. .

RUN chmod +x /opt/drf_project/wait-for-it.sh

