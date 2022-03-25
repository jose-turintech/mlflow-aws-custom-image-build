"""
This module defines the file directory structure
"""
# ────────────────────────────────────────── imports ────────────────────────────────────────── #
from pathlib import Path

from mlflow_custom_serving.conf.base_default_conf import BaseDefaultConf, conf_factory


# ───────────────────────────────────────────────────────────────────────────────────────────── #
#                                      Data Configuration                                       #
# ───────────────────────────────────────────────────────────────────────────────────────────── #

class DataConf(BaseDefaultConf):
    """
    Configuration class of a Data.
    """
    data_path: Path

    def __init__(self, _env_file: str = '.env', **values):
        super().__init__(_env_file, **values)
        self._resolve_paths()

    def _resolve_paths(self):
        """
        Resolve full path of all Path attributes
        """
        for field in self.__fields__:
            value = self.__getattribute__(field)
            self.__setattr__(field, Path(value).resolve() if value else None)


# ───────────────────────────────────────────────────────────────────────────────────────────── #
#                                  Data Configuration Factory                                   #
# ───────────────────────────────────────────────────────────────────────────────────────────── #

def data_conf_factory(_env_file: str = '.env', prefix: str = None, defaults: dict = None, **kwargs) -> DataConf:
    """
    This is a factory generating an DataConf class specific to a service, loading every value from a generic
    .env file storing variables in uppercase with a service prefix.

    example .env:
       PREFIX_DATA_PATH=/tmp/data
       ...
    """
    return conf_factory(config_class=DataConf, _env_file=_env_file, prefix=prefix, defaults=defaults, **kwargs)
