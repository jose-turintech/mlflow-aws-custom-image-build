# mlflow_custom_serving

CustomRest API Serving for mlflow projects

## Description _[TODO]_

What your project can do specifically?

Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features, or a Background
subsection can also be added here.

### Prerequisites

- python
- docker
- docker-compose

> **IMPORTANT**: In order to download the python libraries stored in Nexus, it is necessary that you update
> the [deploy/pip_conf/.netrc](./deploy/pip_conf/.netrc) file with your **access credentials to the Nexus server**.

## Usage _[TODO]_

To deploy the application you must follow the following steps:

1. **Update** the environment files with the appropriate **configuration** for the environment in which you want to
   deploy the APP.  
   Take a look at the [Configuration](#configuration) section for more details.
3. **Build** the docker image: `make app-build`.  
   Take a look at the [Useful scripts](#useful-scripts) and [Deployment steps](#deployment-steps) sections for more
   details.
4. **Deploy** the APP in the configured environment.  
   Take a look at the [Useful scripts](#useful-scripts) and [Deployment steps](#deployment-steps) sections for more
   details.

## Configuration

The values indicated as an example in each of the variables is the value that will be taken by default if you do not
specify that variable in the file '.env'

### Environments

The environment file used by the application depends on the kind of deployment executed.

#### Local

This is the type of deployment that is performed when the application code is executed directly, without packages up it
in a docker container.

In this case, the configuration is getting from **[./deploy/.env](./deploy/.env)** file. This file is referenced in
the [./deploy/Makefile](./deploy/Makefile) by the **_CNF_** field.

This file also contains the default settings for all environments.

#### Development

The application will be packaged in a docker container with the configuration of the development environment by
executing the `make app-deploy-dev` instruction and will use the configuration defined in
the **[./deploy/environments/dev](./deploy/environments/dev)** folder.

The values indicated in the files in this directory will overwrite the values established by default.

The [./deploy/environments/dev/.env](./deploy/environments/dev/.env) file is referenced in
the [./deploy/Makefile](./deploy/Makefile) by the **_CNF_ENV_** field.

#### Production

The application will be packaged in a docker container with the configuration of the production environment by executing
the `make app-deploy-prod` instruction and will use the configuration defined in
the **[./deploy/environments/prod](./deploy/environments/prod)** folder.

The values indicated in the files in this directory will overwrite the values established by default.

The [./deploy/environments/prod/.env](./deploy/environments/prod/.env) file is referenced in
the [./deploy/Makefile](./deploy/Makefile) by the **_CNF_ENV_** field.

### Environment values to specify in the .env file

#### Docker build and deploy configurations

| Variable              | Description                                                     | Default value             |
| --------------------- | --------------------------------------------------------------- | ------------------------- |
| APP_ENV               | Name of the configured deployment environment. <br> E.g. DEV, PRE-PRO, PRO, TST |           |
| APP_GROUP             | Name of the group to which the application belongs.<br>This value will be part of the name of the docker image.| turintech |
| APP_NAME              | Application name.<br>This value will be part of the name of the docker image. | mlflow_custom_serving |
| APP_VERSION           | Application version.<br>This value will be the version of the docker image. | 0.0.0     |
| APP_ID                | Name that identifies the deployed application.<br>This will be used as the name of the docker container. | turintech-mlflow_custom_serving |

#### Logging configuration

For more details, see [loguru](https://loguru.readthedocs.io/en/stable/api/logger.html)

| Variable              | Description                                                     | Default value             |
| --------------------- | --------------------------------------------------------------- | ------------------------- |
| LOGGER_SINK           | Path to the log file                               | /tmp/mlflow_custom_serving/logs/mlflow_custom_serving.log |
| LOGGER_LEVEL          | The minimum severity level from which logged messages should be sent to the sink. <br> - Options: `critical, error, warning, success, info, debug, trace` | INFO |
| LOGGER_ROTATION       | A condition indicating whenever the current logged file should be closed and a new one started. | "12:00"  # New file is created each day at noon |
| LOGGER_RETENTION      | A directive filtering old files that should be removed during rotation or end of program. | "1 month" |

## Useful scripts

- [Makefile](setup/Makefile): This file defines a set of tasks to be executed using the `make` utility.

    ```commandline
    (env-py38-mlflow_custom_serving) user@pc:~/mlflow_custom_serving$ make
     Usage: make <task>
       task options:
            help                           This help.
            clean                          Remove junk files.
            clean-pyc                      Remove Python file artifacts.
            req-install-dev                Install only development requirements in the activated local environment
            req-install                    Install the required libraries.
            req-remove                     Uninstall all the libraries installed in the Python environment.
            req-clean                      Remove all items from the pip cache.
            lint                           Check style with flake8 and pylint.
            test                           Run tests quickly with the default Python.
            app-build                      Build the docker image.
            app-config-dev                 Prints the resolved development application config to the terminal.
            app-deploy-dev                 Deploy the development services.
            app-stop-dev                   Stops running development containers without removing them.
            app-down-dev                   Bring everything of development environment down, removing the containers entirely and the data volumes.
            app-config-prod                Prints the resolved production application config to the terminal.
            app-deploy-prod                Deploy the production services.
            app-stop-prod                  Stops running production containers without removing them.
            app-down-prod                  Bring everything of production environment down, removing the containers entirely and the data volumes.
    ```

## Development and Deployment

### Basic development steps

1. **Activate a Python virtual environment**: `conda activate env-py38`

    ```commandline
    user@pc:~/mlflow_custom_serving$ conda activate env-py38
    (env-py38) user@pc:~/user/mlflow_custom_serving$ 
    ```

1. **Install the project requirements**: `make req-install`

    ```commandline
    (env-py38) user@pc:~/user/mlflow_custom_serving$ make req-install 
    make[1]: Entering directory '/home/user/mlflow_custom_serving'
    ──────────────────────────────────────────────────────────────────────────────────────────────────────────
    ─── Install requirements: requirements.txt requirements_develop.txt 
    ──────────────────────────────────────────────────────────────────────────────────────────────────────────
   
    [...]
   
    pip freeze > /home/user/mlflow_custom_serving/setup/requirements_freeze.txt
    make[1]: Leaving directory '/home/user/mlflow_custom_serving'
    ```

1. **Check the quality of the code**: `make lint`

    ```commandline
    (env-py38) user@pc:~/user/mlflow_custom_serving$ make lint
    
    ────────────────────────────────────────────────────────────────────────────────────────────────────────────
    ─── Checking the project code style [flake8]
    ────────────────────────────────────────────────────────────────────────────────────────────────────────────
    
    ────────────────────────────────────────────────────────────────────────────────────────────────────────────
    ─── Checking the project code style [pylint]
    ────────────────────────────────────────────────────────────────────────────────────────────────────────────
    
    --------------------------------------------------------------------
    Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)
    ```

1. **Running the tests**: `make test`

    ```commandline
    (env-py38) user@pc:~/user/mlflow_custom_serving$ make test
    =================================================================================== test session starts ===================================================================================
    platform linux -- Python 3.8.11, pytest-6.1.2, py-1.10.0, pluggy-0.13.1 -- /home/user/.conda/envs/env-py38/bin/python
    rootdir: /home/user/mlflow_custom_serving/src/mlflow_custom_serving/tests, configfile: pytest.ini
    plugins: cov-2.12.1
    collected 23 items                                                                                                                                                                                                                                              
    
    tests_app_template/tests_conf/test_app_conf.py::TestAppConf::test_default_app_conf PASSED                                                                                       [  4%]
        [...]
    tests_app_template/tests_utils/test_formatting_utils.py::TestFormattingUtils::test_get_data_formatter_4 PASSED                                                                  [100%]
    
    ---------- coverage: platform linux, python 3.8.11-final-0 -----------
    Name                                                                                                         Stmts   Miss Branch BrPart  Cover
    ----------------------------------------------------------------------------------------------------------------------------------------------
    /home/user/mlflow_custom_serving/src/mlflow_custom_serving/src/app_template/__init__.py                     0      0      0      0   100%
        [...]
    /home/user/mlflow_custom_serving/src/mlflow_custom_serving/src/app_template/utils/file_utils.py            15      0      4      0   100%
    /home/user/mlflow_custom_serving/src/mlflow_custom_serving/src/app_template/utils/formatting_utils.py      42      0     20      0   100%
    ----------------------------------------------------------------------------------------------------------------------------------------------
    TOTAL                                                                                                          195     18     54      0    92%
    Coverage HTML written to dir ../docs/coverage
    
    
    =================================================================================== 82 passed in 2.27s ===================================================================================

    ```

      > **NOTE:**
      >
      > Note that if you want to run the tests in debug mode in pycharm, you should disable the coverage
      > in [pytest.ini](./tests/pytest.ini). Otherwise, the execution will not stop at the checkpoints.
      >
      > https://pytest-cov.readthedocs.io/en/latest/debuggers.html

1. **Verification that the log files are generated**: `ls /tmp/mlflow_custom_serving/logs/`

    ```commandline
    (env-py38) user@pc:~/user/mlflow_custom_serving$ ls /tmp/mlflow_custom_serving/logs/
    mlflow_custom_serving.log
    ```

### Deployment steps

1. **Validate and view the Compose file with development configuration**: `make app-config-[dev, prod]`

   ```commandline
   (env-py38) user@pc:~/user/mlflow_custom_serving$  make app-config-dev 
   make[1]: Entering directory '/home/user/mlflow_custom_serving'
   services:
     app:
       build:
         args:
           NETRC_PATH: ./deploy/pip_conf/.netrc
           PIP_CONF_PATH: ./deploy/pip_conf/pip.conf
         context: /home/user/mlflow_custom_serving
         dockerfile: ./deploy/Dockerfile
       container_name: turintech-mlflow_custom_serving-DEV
       environment:
         APP_ENV: DEV
         APP_GROUP: turintech
         APP_ID: turintech-mlflow_custom_serving-DEV
         APP_NAME: mlflow_custom_serving
         APP_VERSION: 0.0.0
         LOGGER_LEVEL: DEBUG
         LOGGER_SINK: /logs/DEV/mlflow_custom_serving.log
         NETRC_PATH: ./deploy/pip_conf/.netrc
         PIP_CONF_PATH: ./deploy/pip_conf/pip.conf
       image: turintech/mlflow_custom_serving:0.0.0
       ports:
       - published: 81
         target: 5001
       restart: always
       volumes:
       - /home/user/mlflow_custom_serving/src:/app:rw
       - /home/user/mlflow_custom_serving/docker/logs:/logs:rw
   version: '3.9'
   
   make[1]: Leaving directory '/home/user/mlflow_custom_serving'
   ```

1. **Update Nexus credentials**: You can update the [.netrc](./deploy/pip_conf/.netrc) file manually or running the
   following command: `deploy/make replace-pip-conf`

    ```commandline
    user@pc:~/mlflow_custom_serving$ cd deploy/
    
    user@pc:~/mlflow_custom_serving/deploy$ make
    Usage: make [ENV=<dev prod>] [CNF=globalEnvFile] [CNF_ENV=environmentEnvFile]  <task>
      task options:
           help                           This help.
           app-config                     Prints the resolved application config to the terminal. >>> USE: make app-config [ENV=envName]
           app-build                      Build the docker image. >>> USE: make app-build [ENV=envName]
           app-build-nc                   Build the images without caching. >>> USE: make app-build-nc [ENV=envName]
           app-deploy                     Deploy the services. >>> USE: make app-deploy ENV=envName MODEL
           app-stop                       Stops running containers without removing them. >>> USE: make app-stop ENV=envName
           app-down                       Bring everything down, removing the containers entirely and the data volumes. >>> USE: make app-down ENV=envName
           app-restart                    Stop running containers and Spin up again the project. >>> USE: make app-restart ENV=envName
           replace-pip-conf               Replaces the current PyPI configuration with the one found in the deployment machine
    
    user@pc:~/mlflow_custom_serving/deploy$ make replace-pip-conf 
    Updated the '/home/user/mlflow_custom_serving/deploy/pip_conf/.netrc' file with the content of the '~/.netrc' file
    Updated the '/home/user/mlflow_custom_serving/deploy/pip_conf/pip.conf' file with the content of the '~/.config/pip/pip.conf' file
    ```

1. **Build the application**: `make app-build`

    ```commandline
    user@pc:~/mlflow_custom_serving$ make app-build
    make[1]: Entering directory '/home/user/mlflow_custom_serving'
    Building app
    #1 [internal] load build definition from Dockerfile
    #1 sha256:e010713e9a26d632588b22329c7ee0880370875384c32fff52199126c8ab72e2
    #1 transferring dockerfile: 4.09kB done
    #1 DONE 0.0s
    
        [...]
    
    #7 [2/7] WORKDIR /app
    #7 sha256:2c9d949b0f73871b396f7add33b8527b02605e1f0a68d301ce99f18b1e883037
    #7 CACHED
    
        [...]
    
    #13 [7/7] COPY ./src /app
    #13 sha256:1714c122dd08e34ab4d3330507eb86ee98e8ec3cc069b7d328150c8ce2af08a2
    #13 DONE 0.1s
    
    #14 exporting to image
    #14 sha256:e8c613e07b0b7ff33893b694f7759a10d42e180f2b4dc349fb57dc6b71dcab00
    #14 exporting layers
    #14 exporting layers 0.4s done
    #14 writing image sha256:287bbd45668c16907f8e091a7d81838cbc34fcf853c7a9c7e167093338fed3a5 done
    #14 naming to docker.io/turintech/mlflow_custom_serving:0.0.0 done
    #14 DONE 0.4s
    make[1]: Leaving directory '/home/user/mlflow_custom_serving'
    ```

1. **Verifying that images have been created**: `docker images`

    ```commandline
    user@pc:~/mlflow_custom_serving$ docker images
    REPOSITORY                 TAG       IMAGE ID       CREATED         SIZE
    turintech/mlflow_custom_serving   0.0.0     287bbd45668c   5 minutes ago   183MB
    ```

1. **Deploy the Application with development configuration**: `make app-deploy-dev`

    ```commandline
    user@pc:~/mlflow_custom_serving$ make app-deploy-dev 
    make[1]: Entering directory '/home/user/mlflow_custom_serving'
    Creating network "turintech-mlflow_custom_serving-dev_default" with the default driver
    Creating turintech-mlflow_custom_serving-DEV ... done
    
    You can see the log traces by running the following command:
            docker logs --tail 100 -f turintech-mlflow_custom_serving-DEV
    
    You can access to the docker container by running the following command:
            docker exec -it turintech-mlflow_custom_serving-DEV bash
    
    make[1]: Leaving directory '/home/user/mlflow_custom_serving'
    ```
   
      On the other hand, if what you want is to display the production version, it should execute the following command:

    ```commandline
    user@pc:~/mlflow_custom_serving$ make app-deploy-prod 
    make[1]: Entering directory '/home/user/mlflow_custom_serving'
    Creating network "turintech-mlflow_custom_serving-dev_default" with the default driver
    Creating turintech-mlflow_custom_serving ... done
    
    You can see the log traces by running the following command:
            docker logs --tail 100 -f turintech-mlflow_custom_serving
    
    You can access to the docker container by running the following command:
            docker exec -it turintech-mlflow_custom_serving bash
    
    make[1]: Leaving directory '/home/user/mlflow_custom_serving'
    ```   

1. **Verifying that docker containers have been created**: `docker ps -a`

    ```commandline
    user@pc:~/mlflow_custom_serving$ docker ps -a
    CONTAINER ID   IMAGE                            COMMAND                  CREATED          STATUS          PORTS                                   NAMES
    1cc4484afd2f   turintech/mlflow_custom_serving:0.0.0   "python -u ./mlflow_custom_serving"   3 seconds ago        Up 1 second                   turintech-mlflow_custom_serving
    5f69c389af56   turintech/mlflow_custom_serving:0.0.0   "python -u ./mlflow_custom_serving"   About a minute ago   Up About a minute             turintech-mlflow_custom_serving-DEV
    ```

1. **Connect to the container and check its content**: `docker exec -it turintech-mlflow_custom_serving-DEV bash`

    ```commandline
    user@pc:~/mlflow_custom_serving$  docker exec -it turintech-mlflow_custom_serving-DEV bash
    root@5f69c389af56:/app# ls /
    app  bin  boot  dev  etc  home  lib  lib64  logs  media  mnt  opt  proc  root  run  sbin  setup  srv  sys  tmp  usr  var
    root@5f69c389af56:/app# ls
    __about__.py  mlflow_custom_serving
    root@5f69c389af56:/app# ls /setup/
    requirements.txt
    root@5f69c389af56:/app# ls /logs/
    mlflow_custom_serving.log
    root@5f69c389af56:/app# exit
    exit
    ```

1. **Check the log traces**: `docker logs --tail 100 -f turintech-mlflow_custom_serving-DEV`

    ```commandline
    user@pc:~/mlflow_custom_serving$ docker logs --tail 100 -f turintech-mlflow_custom_serving-DEV
    2021-08-03 13:37:05.112 - INFO     - __main__.print_conf:16 - Configuration Manager
    2021-08-03 13:37:05.112 - INFO     - __main__.print_conf:17 -  - path_root : /
    2021-08-03 13:37:05.113 - INFO     - __main__.print_conf:18 -  - path_src  : /app
    2021-08-03 13:37:05.113 - INFO     - __main__.print_conf:19 -  - path_app  : /app/mlflow_custom_serving
    2021-08-03 13:37:05.114 - INFO     - __main__.print_conf:20 -  - path_conf : /app/mlflow_custom_serving/conf
    2021-08-03 13:37:05.114 - INFO     - __main__.print_conf:21 -  - env_file  : /app/.env
    2021-08-03 13:37:10.120 - INFO     - __main__.main:27 - 2021-08-03 13:37:10.120464
    2021-08-03 13:37:15.126 - INFO     - __main__.main:27 - 2021-08-03 13:37:15.126420
    2021-08-03 13:37:20.132 - INFO     - __main__.main:27 - 2021-08-03 13:37:20.132329
    2021-08-03 13:37:25.138 - INFO     - __main__.main:27 - 2021-08-03 13:37:25.138371
    ```

1. **Stop the application**: `make app-stop-dev`

    ```commandline
    user@pc:~/mlflow_custom_serving$ make app-stop-dev 
    make[1]: Entering directory '/home/user/mlflow_custom_serving'
    Stopping turintech-mlflow_custom_serving-DEV ... done
    make[1]: Leaving directory '/home/user/mlflow_custom_serving'
   
    user@pc:~/mlflow_custom_serving$ docker ps -a
    CONTAINER ID   IMAGE                            COMMAND                  CREATED          STATUS                       PORTS                                   NAMES
    1cc4484afd2f   turintech/mlflow_custom_serving:0.0.0   "python -u ./mlflow_custom_serving"   3 minutes ago   Up 3 minutes                           turintech-ap-mlflow_custom_serving
    5f69c389af56   turintech/mlflow_custom_serving:0.0.0   "python -u ./mlflow_custom_serving"   4 minutes ago   Exited (137) 7 seconds ago             turintech-mlflow_custom_serving-DEV
    ```

1. **Remove the application**: `make app-down-dev`

    ```commandline
    user@pc:~/mlflow_custom_serving$ make app-down-dev 
    make[1]: Entering directory '/home/user/mlflow_custom_serving'
    Removing turintech-mlflow_custom_serving-DEV ... done
    Removing network turintech-mlflow_custom_serving-dev_default
    make[1]: Leaving directory '/home/user/mlflow_custom_serving'

    user@pc:~/mlflow_custom_serving$ docker ps -a
    CONTAINER ID   IMAGE                            COMMAND                  CREATED          STATUS          PORTS                                   NAMES
    1cc4484afd2f   turintech/mlflow_custom_serving:0.0.0   "python -u ./app_tem…"   3 minutes ago   Up 3 minutes             turintech-mlflow_custom_serving
    
    user@pc:~/mlflow_custom_serving$ docker images
    REPOSITORY                 TAG               IMAGE ID       CREATED              SIZE
    turintech/mlflow_custom_serving   0.0.0             287bbd45668c   20 minutes ago   183MB
    ```