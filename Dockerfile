FROM python:3.12-bookworm

ENV PYTHONUNBUFFERED 1
ARG REQUIREMENT_FILE

RUN apt update
WORKDIR /code

RUN echo REQUIREMENT_FILE=${REQUIREMENT_FILE}
RUN addgroup spaced_service 

COPY ${REQUIREMENT_FILE} /code/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
