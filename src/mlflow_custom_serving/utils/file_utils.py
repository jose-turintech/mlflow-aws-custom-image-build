# ────────────────────────────────────────── imports ────────────────────────────────────────── #
import json
from pathlib import Path
from typing import List, Dict, Callable, Union, Any

from pydantic import BaseModel

from mlflow_custom_serving.utils.data_utils import JsonType


# ───────────────────────────────────────────────────────────────────────────────────────────── #
#                                        JSON File utils                                        #
# ───────────────────────────────────────────────────────────────────────────────────────────── #


def read_json(file_path: str or Path) -> JsonType:
    """ Return a JSON file data """
    if not Path(file_path).exists():
        raise FileNotFoundError(file_path)
    with open(str(file_path), encoding='utf-8') as file:
        return json.load(file)


def read_json_as_data_model(
        file_path: str or Path, data_model: Callable[[Union[Any, BaseModel]], BaseModel]
) -> List[BaseModel] or BaseModel:
    """
    Read a JSON file and return the information in the indicated data structure

    :param file_path: JSON file path
    :param data_model: (Callable[..., BaseModel]) Class type inheriting from BaseModel to instantiate.
    :return: data_model type
    """
    data = read_json(file_path=file_path)
    return data_model(**data) if isinstance(data, dict) else json_as_data_model_list(data=data, data_model=data_model)


def json_as_data_model_list(
        data: List[Dict], data_model: Callable[[Union[Any, BaseModel]], BaseModel]
) -> List:
    """ Return the information in the indicated data structure """
    return list(map(lambda value: data_model(**value), data))
