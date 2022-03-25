# mlflow_custom_serving

Custom script that uses the mlflow python API in order to customize the behaviour ofthe process that generates the AWS Sagemaker docker image for deployment.

This repository aims to produce a customise the default docker image, provindg a way to enable custom Rest API endpoints in addition to the default endpoints provided by mlflow (ping and invocations).

After a lot of experimentation and reverse engineering of the mlflow it does that by essencially:

- setting a tricky value to the GUNICORN_CMD_ARGS environment variable allowed by mlflow in order to provide additional config parameter to the gunicorn server process. That value is set to point to a custom wsgi app (a PR would be needed in order to modify the mlflow/sagemaker code so it can provide support for custom wsgi servers, that support currently doesn't exist)
- overwriting the default nginx config provided also by mlflow by default (and as the wsi server, hardcoded in the core) so it is replaced at the docker image build stage, by one provided by the custom scoring server (wsgi server) provided in the previous step.
- custom scoring server is implemented as a POC, using a copy, and extension of the default wsgi server, providing an additional endpoint /turing, that listens to get requests responding with a hardcoded json.

The cusstom scoring server for this POC is located in the repo: mlflow-turing-scoring-server. That contains the nginx.conf and the wsgi.py implementation used in this POC.
The use of that requirement is placed under setup/requirements.txt 

## Description

It generates a new docker image on your local registry, that serves as a template for model deployment under AWS SSagemaker using mlflow models.


### Prerequisites

- python
- docker

## Usage

Just install the needed requirements under a new conda env:
- conda create -n mlflow-sagemaker-custom-image python=3.8
- conda activate mlflow-sagemaker-custom-image
- pip install --upgrade pip
- pip install setup/requirements.txt
- pip install setup/requirements_develop.txt
- PYTHONPATH=./src python src/mlflow_custom_serving/main.py

The execution of the program will generate a new image in your local docker registry, with the tagging c7-mlflow-pyfunc-sagemaker

You can check it by executin: docker image ls

After that you can start a container using the image with the following mlflow command:

mlflow sagemaker run-local -m ./fonduer_emmental_model -p 5003 -i c7-mlflow-pyfunc-sagemaker:latest

When the container finish booting up, you can check it's correct behaviour by requesting the custom endpoint via get:

- curl http://localhost:5003/turing

you will see the following response: { turintech: test}

The generated docker image is totally compatible with the existing mlflow code, and can be deployed remotely in AWS, following the same steps documented in the repo mlflow-pyfunc-poc.
It essentially generates the equivalent docker image but customised, so the rest of the steps can be the same.


## Configuration

You can change the behaviour of this POC by changing the nginx.conf or the wsgi.py or __init__.py of the mlflow-turing-scoring-server repository.
Also if further customization is needed, the implementation under the main.py file can be tweaked to change the way the dockerfile for the image is written.
