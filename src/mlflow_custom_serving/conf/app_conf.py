"""
This module defines the Application configuration attributes
"""
# ────────────────────────────────────────── imports ────────────────────────────────────────── #
from pydantic import Field

from mlflow_custom_serving.conf.base_default_conf import BaseDefaultConf, conf_factory


# ───────────────────────────────────────────────────────────────────────────────────────────── #
#                                      APP Configuration                                        #
# ───────────────────────────────────────────────────────────────────────────────────────────── #

class AppConf(BaseDefaultConf):
    """
    This class contains the configuration attributes of the application
    The attributes of this class are updated with the values of the environment variables.
    """

    app_env: str = Field(None, description="Name of the configured deployment environment")
    app_group: str = Field('turintech', description="Name of the group to which the application belongs.")
    app_name: str = Field('mlflow_custom_serving', description="Application name")
    app_version: str = Field('0.0.0', description="Application version")
    app_id: str = Field(None, description="Name that identifies the deployed Application")


# ───────────────────────────────────────────────────────────────────────────────────────────── #
#                                  APP Configuration Factory                                    #
# ───────────────────────────────────────────────────────────────────────────────────────────── #

def app_conf_factory(_env_file: str = '.env', prefix: str = None, defaults: dict = None, **kwargs) -> AppConf:
    """
    This is a factory generating an AppConf class specific to a service, loading every value from a generic
    .env file storing variables in uppercase with a service prefix.

    example .env:
       PREFIX_APP_ENV='DEV'
       PREFIX_APP_VERSION='1.0.0'
       ...
    """
    return conf_factory(config_class=AppConf, _env_file=_env_file, prefix=prefix, defaults=defaults, **kwargs)
