"""
This module aims to implement the tests of the file_utils module
"""
# ────────────────────────────────────────── imports ────────────────────────────────────────── #
from pathlib import Path

import pytest
from pydantic import BaseModel

from mlflow_custom_serving.utils import file_utils

from tests_mlflow_custom_serving.base.base_test import BaseTest
from tests_mlflow_custom_serving.conftest import data_mgr


# ───────────────────────────────────────────────────────────────────────────────────────────── #
#                                         Test Class                                            #
# ───────────────────────────────────────────────────────────────────────────────────────────── #

class Example(BaseModel):
    first_field: str
    second_field: int


class TestFileUtils(BaseTest):
    """
    file_utils.py testing class
    """

    _data_path: Path = data_mgr.utils_path.joinpath('file_utils')

    def test_read_json(self):
        """
        This method validates the file_utils.read_json method
        """
        expected = {"first_field": "value", "second_field": 1}
        result = file_utils.read_json(file_path=self._data_path.joinpath("example_dict.json"))
        self.assert_dict(expected=expected, result=result)

    def test_read_json_as_data_model_dict(self):
        """
        This method validates the file_utils.read_json_as_data_model method when the file contains a dict
        """
        expected = {"first_field": "value", "second_field": 1}
        result = file_utils.read_json_as_data_model(
            file_path=self._data_path.joinpath("example_dict.json"), data_model=Example)
        self.assert_dict(expected=expected, result=result, by_alias=True)

    def test_read_json_as_data_model_list(self):
        """
        This method validates the file_utils.read_json_as_data_model method when the file contains a list of dicts
        """
        expected = [{"first_field": "value1", "second_field": 1}, {"first_field": "value2", "second_field": 2}]
        result = file_utils.read_json_as_data_model(
            file_path=self._data_path.joinpath("example_list.json"), data_model=Example)
        self.assert_list(expected=expected, result=result, by_alias=True)

    def test_read_json_as_data_model_empty(self):
        """
        This method validates the file_utils.read_json_as_data_model method when the file doesn't exist
        """
        with pytest.raises(FileNotFoundError) as error:
            file_utils.read_json_as_data_model(file_path=self._data_path.joinpath("not_found.json"), data_model=Example)
        self.case.assertEqual(str(self._data_path.joinpath("not_found.json")), str(error.value))


# ───────────────────────────────────────────────────────────────────────────────────────────── #

if __name__ == "__main__":
    pytest.main()
