"""
This module implements useful methods for data treatment
"""
# ────────────────────────────────────────── imports ────────────────────────────────────────── #
from datetime import datetime
from enum import Enum, EnumMeta
from pathlib import Path
from typing import List, Union, Dict, Any

from pydantic import BaseModel

# ───────────────────────────────────────────────────────────────────────────────────────────── #
#                               Definition of generic data types                                #
# ───────────────────────────────────────────────────────────────────────────────────────────── #

JsonType = Union[List[Dict], Dict, BaseModel]


# ───────────────────────────────────────────────────────────────────────────────────────────── #
#                                            Lists                                              #
# ───────────────────────────────────────────────────────────────────────────────────────────── #


def join_values(values: List[str], union: str = '') -> str:
    """
    Joins all the strings in the list by means of the string indicated in "union", filtering those null or empty values
    """
    return union.join(list(filter(lambda value: value, values)))


# ───────────────────────────────────────────────────────────────────────────────────────────── #
#                                       Serializing data                                        #
# ───────────────────────────────────────────────────────────────────────────────────────────── #

def serialize_data(data: Any, date_format: str = '%Y-%m-%d %H:%M:%S', by_alias: bool = False):
    """ Serialize any type of data """
    kwargs = dict(date_format=date_format, by_alias=by_alias)
    if isinstance(data, dict):
        return {
            serialize_data(key, **kwargs): serialize_data(value, **kwargs)
            for key, value in data.items()
        }
    if isinstance(data, (list, tuple)):
        return [serialize_data(data=value, **kwargs) for value in data]
    if isinstance(data, datetime):
        return data.strftime(date_format)
    if isinstance(data, (Enum, EnumMeta)):
        return data.value
    if isinstance(data, BaseModel):
        return serialize_data(data=data.dict(by_alias=by_alias), **kwargs)
    if isinstance(data, type):
        return str(data)
    if isinstance(data, Path):
        return str(data)
    return data
