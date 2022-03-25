# syntax = docker/dockerfile:1
FROM python:3.8-slim-buster

LABEL maintainer="Turing Intelligence Technology <jose@turintech.ai>"

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# ─── WORKDIR and ARGS
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────

# set the working directory in the container
WORKDIR /app



# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# ─── Dependencies installation
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────

# update linux system and install gcc packages
RUN apt-get update && \
    apt-get install -y python3-dev build-essential

# instlal Git
RUN apt-get install -y git

# update pip
RUN pip install --upgrade pip

# copy the the Nexus credentials
ARG NETRC_PATH=./deploy/pip_conf/.netrc
ARG PIP_CONF_PATH=./deploy/pip_conf/pip.conf
COPY $PIP_CONF_PATH /etc/pip.conf
COPY $NETRC_PATH /root/.netrc
RUN chmod 0600 /root/.netrc

# copy and install generic PyPI dependencies
COPY setup/requirements.txt /setup/requirements.txt
RUN pip install -r /setup/requirements.txt

# remove the credentials file
RUN rm -rf /root/.netrc


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# ─── COPY source code
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────

# copy the source code to the working directory
COPY ./src /app


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# ─── Execution command
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────

# Python interpreter
ENV PYTHONPATH='/app/:$PYTHONPATH'
ENTRYPOINT ["python"]

# command to run on container start
# "-u" send the "print" output to docker logs
CMD ["-u", "./mlflow_custom_serving/main.py" ]
