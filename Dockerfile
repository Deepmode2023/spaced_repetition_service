FROM python:3.12-bookworm

ENV PYTHONUNBUFFERED 1
ARG REQUIREMENT_FILE

RUN apt update
WORKDIR /code
RUN echo ${REQUIREMENT_FILE}

COPY ${REQUIREMENT_FILE} /code/requirements.txt
COPY ./alembic /code/alembic/
COPY alembic.ini /code/alembic.ini
COPY ./app /code/app/

RUN apt-get install -y postgresql-client
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt
