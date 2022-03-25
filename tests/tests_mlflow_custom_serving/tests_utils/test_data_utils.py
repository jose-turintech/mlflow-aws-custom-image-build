"""
This module aims to implement the tests of the data_utils module
"""
# ────────────────────────────────────────── imports ────────────────────────────────────────── #
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Type, Tuple

import pytest
from pydantic import BaseModel

from mlflow_custom_serving.utils.data_utils import join_values, serialize_data

from tests_mlflow_custom_serving.base.base_test import BaseTest


# ───────────────────────────────────────────────────────────────────────────────────────────── #
#                                         Test Class                                            #
# ───────────────────────────────────────────────────────────────────────────────────────────── #

class ExampleEnum(Enum):
    ENUM_1 = "value_1"
    ENUM_2 = "value_2"
    ENUM_3 = "value_3"


class Example(BaseModel):
    field_alias: Type = str
    field1: str = "field1"
    field2: dict = dict(key1=dict(key1="value1", key2="value2", value3=[]))
    field3: datetime = datetime(2014, 3, 5, 20, 13, 50)
    field4: Path = Path(__file__)
    field5: Tuple[str, int] = ("value", 1)
    field6: ExampleEnum = ExampleEnum.ENUM_2


class TestDataUtils(BaseTest):
    """
    data_utils.py testing class
    """

    date_format: str = '%Y-%m-%d %H:%M:%S'

    def test_join_values(self):
        """
        This method validates the data_utils.join_values method
        """
        values = [None, "value1", "", "value3", None, "value5", "value6"]
        expected = "value1.value3.value5.value6"
        self.case.assertEqual(expected, join_values(values=values, union="."))

    def test_serialize_data(self):
        """
        This method validates the data_utils.serialize_data method
        """
        serialized_data = serialize_data(data=Example(), date_format=self.date_format, by_alias=True)
        expected = dict(
            field1='field1',
            field2=dict(key1=dict(key1="value1", key2="value2", value3=[])),
            field3='2014-03-05 20:13:50',
            field4=str(Path(__file__)),
            field5=['value', 1],
            field_alias="<class 'str'>",
            field6="value_2"
        )
        self.assert_dict(expected=expected, result=serialized_data)


# ───────────────────────────────────────────────────────────────────────────────────────────── #

if __name__ == "__main__":
    pytest.main()
