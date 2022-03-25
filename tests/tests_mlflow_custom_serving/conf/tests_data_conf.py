"""
This module defines the file directory structure
"""
# ────────────────────────────────────────── imports ────────────────────────────────────────── #
from pathlib import Path

from mlflow_custom_serving.conf.base_default_conf import conf_factory
from mlflow_custom_serving.conf.data_conf import DataConf


# ───────────────────────────────────────────────────────────────────────────────────────────── #
#                                      Data Configuration                                       #
# ───────────────────────────────────────────────────────────────────────────────────────────── #


class TestsDataConf(DataConf):
    """
    Configuration class of a Data.
    """

    endpoints_path: Path = None
    rest_data_models_path: Path = None
    utils_path: Path = None

    def _update_empty_values(self):
        """
        Updating the attributes for which its value has not been indicated through the environment variables.
        """
        if self.data_path:
            if not self.endpoints_path:
                self.endpoints_path = self.data_path.joinpath("endpoints")
            if not self.rest_data_models_path:
                self.rest_data_models_path = self.data_path.joinpath("rest_data_models")
            if not self.utils_path:
                self.utils_path = self.data_path.joinpath("utils")


# ───────────────────────────────────────────────────────────────────────────────────────────── #
#                                  Data Configuration Factory                                   #
# ───────────────────────────────────────────────────────────────────────────────────────────── #

def tests_data_conf_factory(
        _env_file: str = '.env', prefix: str = None, defaults: dict = None, **kwargs
) -> TestsDataConf:
    """
    This is a factory generating an DataConf class specific to a service, loading every value from a generic
    .env file storing variables in uppercase with a service prefix.

    example .env:
       PREFIX_DATA_PATH=/tmp/data
       ...
    """
    return conf_factory(config_class=TestsDataConf, _env_file=_env_file, prefix=prefix, defaults=defaults, **kwargs)
