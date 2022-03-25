FROM python:3.8

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install mlflow
RUN pip install gevent>=1.4.0