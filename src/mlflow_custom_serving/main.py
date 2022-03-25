"""
This module contains the main process
"""
# ────────────────────────────────────────── imports ────────────────────────────────────────── #
import os
from datetime import datetime
from time import sleep

import mlflow
from loguru import logger
from mlflow.utils import cli_args
from pkg_resources import resource_filename
import shutil

from mlflow_custom_serving.conf.conf_manager import conf_mgr
import mlflow_turing_scoring_server
from mlflow.sagemaker import cli


# ───────────────────────────────────────────────────────────────────────────────────────────── #

def print_conf():
    logger.info("Configuration Manager")
    logger.info(f" - path_root : {conf_mgr.path_root}")
    logger.info(f" - path_src  : {conf_mgr.path_src}")
    logger.info(f" - path_app  : {conf_mgr.path_app}")
    logger.info(f" - path_conf : {conf_mgr.path_conf}")
    logger.info(f" - env_file  : {conf_mgr.env_file}")


def main():
    print("This is my test.")
    build_and_push_container(True, False, "c7-mlflow-pyfunc-sagemaker", None)


@cli_args.MLFLOW_HOME
def build_and_push_container(build, push, container, mlflow_home):
    """
    Build new MLflow Sagemaker image, assign it a name, and push to ECR.

    This function builds an MLflow Docker image.
    The image is built locally and it requires Docker to run.
    The image is pushed to ECR under current active AWS account and to current active AWS region.
    """
    if not (build or push):
        print("skipping both build and push, have nothing to do!")
    if build:
        sagemaker_image_entrypoint = """
        ENTRYPOINT ["python", "-c", "import sys; from mlflow.models import container as C; \
        C._init(sys.argv[1])"]
        """

        def setup_container(cwd):
            # Copy the nginx.conf from the model of from the mlflow_custom_scoring_server module.
            # so we can replace the default existing nginx.conf that mlflow provides for deployment.
            print("Value of calculated working directory: "+cwd)
            turing_nginx_conf = resource_filename(
               mlflow_turing_scoring_server.__name__, "scoring_server/nginx.conf"
            )
            shutil.copy(turing_nginx_conf, cwd)
            # 'RUN sed -i \'s/invocations/invocations|turing/g\' /miniconda/lib/python3.9/site-packages/mlflow/models/container/scoring_server/nginx.conf',

            return "\n".join(
                [
                    'COPY nginx.conf /miniconda/lib/python3.9/site-packages/mlflow/models/container/scoring_server/nginx.conf',
                    'ENV GUNICORN_CMD_ARGS="--timeout 60 -k gevent -- mlflow_turing_scoring_server.scoring_server.wsgi:app"',
                    'ENV {disable_env}="false"',
                    'RUN python -c "from mlflow.models.container import _install_pyfunc_deps;'
                    '_install_pyfunc_deps(None, False)"',
                ]
            )

        mlflow.models.docker_utils._build_image(
            container,
            mlflow_home=os.path.abspath(mlflow_home) if mlflow_home else None,
            entrypoint=sagemaker_image_entrypoint,
            custom_setup_steps_hook=setup_container,
        )
    if push:
        mlflow.sagemaker.push_image_to_ecr(container)


if __name__ == '__main__':
    print_conf()
    main()
