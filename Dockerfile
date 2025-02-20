FROM python:3.12-bookworm

ENV PYTHONUNBUFFERED 1
ARG REQUIREMENT_FILE

RUN apt update
WORKDIR /code

COPY ${REQUIREMENT_FILE} /code/app/config/requirements.txt
COPY ./alembic /code/alembic/
COPY alembic.ini /code/alembic.ini
COPY ./app /code/app/

RUN apt-get install -y postgresql-client
RUN pip install --upgrade pip
RUN pip install -r ./app/config/requirements.txt
