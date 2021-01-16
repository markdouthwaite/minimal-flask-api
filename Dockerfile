FROM python:3.7.8-slim

EXPOSE 5000

RUN useradd demo

COPY requirements requirements
RUN pip install -U pip && pip install -r requirements/core.txt

COPY ./src /app/src
COPY ./bin /app/bin
WORKDIR /app

ENTRYPOINT ["bash", "/app/bin/run.sh"]