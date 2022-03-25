"""
This module defines the common attributes necessary for the treatment of application logs.
"""
# ────────────────────────────────────────── imports ────────────────────────────────────────── #
from datetime import time, timedelta
from pathlib import Path
from typing import Union, Optional

from pydantic import validator

from mlflow_custom_serving.conf.base_default_conf import BaseDefaultConf, conf_factory


# ───────────────────────────────────────────────────────────────────────────────────────────── #
#                                    Logging Configuration                                      #
# ───────────────────────────────────────────────────────────────────────────────────────────── #

class LoggerConf(BaseDefaultConf):
    """
    This class contains the configuration attributes of the application logs.
    The attributes of this class are updated with the values of the environment variables.

    - sink: An object in charge of receiving formatted logging messages and propagating them to an appropriate endpoint.
    - level: The minimum severity level from which logged messages should be sent to the sink.
    - format: The template used to format logged messages before being sent to the sink.
    - colorize: Whether the color markups contained in the formatted message should be converted to ansi codes for
            terminal coloration, or stripped otherwise. If None, the choice is automatically made based on the sink
            being a tty or not.
    - serialize: Whether the logged message and its records should be first converted to a JSON string before being
            sent to the sink.
    - backtrace: Whether the exception trace formatted should be extended upward, beyond the catching point, to show
            the full stacktrace which generated the error.
    - diagnose: Whether the exception trace should display the variables values to eases the debugging.
            This should be set to False in production to avoid leaking sensitive data.
    - enqueue: Whether the messages to be logged should first pass through a multiprocess-safe queue before reaching
            the sink. This is useful while logging to a file through multiple processes.
            This also has the advantage of making logging calls non-blocking.

    Only on logs directed to file path outputs:
    - rotation: A condition indicating whenever the current logged file should be closed and a new one started.
    - retention: A directive filtering old files that should be removed during rotation or end of program.
    - compression: A compression or archive format to which log files should be converted at closure.
    - delay: Whether the file should be created as soon as the sink is configured, or delayed until first
            logged message. It defaults to False.
    """

    sink: Union[str, object, Path]

    level: str = "INFO"
    format: str = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>" \
                  " <r>-</r> <level>{level: <8}</level>" \
                  " <r>-</r> <cyan>{name}</cyan>.<cyan>{function}</cyan>:<cyan>{line}</cyan>" \
                  " <r>-</r> <level>{message}</level>"
    colorize: Optional[bool] = True
    serialize: Optional[bool] = False
    backtrace: Optional[bool] = True
    diagnose: Optional[bool] = False
    enqueue: Optional[bool] = True

    @validator('level')
    def upper_validator(cls, value: str):
        return value.upper() if value else value


class FileLoggerConf(LoggerConf):
    colorize: Optional[bool] = False
    rotation: Union[str, int, time, timedelta] = "12:00"  # New file is created each day at noon
    retention: Union[str, int, time, timedelta] = "1 month"
    compression: Optional[str] = "zip"
    delay: bool = True


# ───────────────────────────────────────────────────────────────────────────────────────────── #
#                                Logging Configuration Factory                                  #
# ───────────────────────────────────────────────────────────────────────────────────────────── #

def logger_conf_factory(_env_file: str = '.env', prefix: str = None, defaults: dict = None, **kwargs) -> LoggerConf:
    """
    This is a factory generating an LoggerConf class specific to a service, loading every value from a generic
    .env file storing variables in uppercase with a service prefix.

    example .env:
       PREFIX_LEVEL=INFO
       ...
    """
    return conf_factory(config_class=LoggerConf, _env_file=_env_file, prefix=prefix, defaults=defaults, **kwargs)


def file_logger_conf_factory(
        _env_file: str = '.env', prefix: str = None, defaults: dict = None, **kwargs
) -> FileLoggerConf:
    """
    This is a factory generating an FileLoggerConf class specific to a service, loading every value from a generic
    .env file storing variables in uppercase with a service prefix.

    example .env:
       PREFIX_LEVEL=INFO
       ...
    """
    return conf_factory(config_class=FileLoggerConf, _env_file=_env_file, prefix=prefix, defaults=defaults, **kwargs)
