"""
This module aims to implement the base class used by all test classes with common methods.
"""
# ────────────────────────────────────────── imports ────────────────────────────────────────── #
import unittest
from collections import OrderedDict
from pathlib import Path
from typing import Any, List

import pytest
from loguru import logger
from pydantic import BaseModel
from pydantic.fields import ModelField

from mlflow_custom_serving.utils.data_utils import serialize_data
from mlflow_custom_serving.utils.file_utils import read_json

from tests_mlflow_custom_serving.conftest import data_mgr


# ───────────────────────────────────────────────────────────────────────────────────────────── #
#                                        Base Test Class                                        #
# ───────────────────────────────────────────────────────────────────────────────────────────── #

class BaseTest:
    """
    Base Tests Class
    """

    case = unittest.TestCase()
    method: str = None

    _data_path: Path = data_mgr.data_path

    # -------------------------------------------------------------------------------------------

    @classmethod
    def setup_class(cls):
        """ Configuration called when initializing the class """

    @classmethod
    def teardown_class(cls):
        """ Configuration called when destroying the class """

    def setup_method(self, method):
        """ Configuration called for every method """
        self.method = method.__name__

    def teardown_method(self, method):
        """ Configuration called at the end of the method execution """

    # -------------------------------------------------------------------------------------------

    def serialize_data(self, data: Any, by_alias: bool = False):
        """ Serialize any type of data so that it can be compared """
        if isinstance(data, ModelField):
            return self.serialize_data(
                data=dict(name=data.name, alias=data.alias, type=data.outer_type_, required=data.required),
                by_alias=by_alias)
        return serialize_data(data=data, by_alias=by_alias)

    def sorted_serialize_data(self, data: Any, by_alias: bool = False):
        """ Serialize and sort any type of data so that it can be compared """
        serialized_data = self.serialize_data(data=data, by_alias=by_alias)
        if isinstance(data, dict):
            return dict(OrderedDict(sorted(serialized_data.items())))
        if isinstance(data, list):
            return sorted(serialized_data)
        return serialized_data

    # -------------------------------------------------------------------------------------------

    def assert_dict(
            self, expected: dict or BaseModel, result: dict or BaseModel, by_alias: bool = False, msg: str = None
    ):
        """ Serialize the dictionaries and check that they are equal """
        expected_serialized = self.sorted_serialize_data(data=expected, by_alias=by_alias)
        result_serialized = self.sorted_serialize_data(data=result, by_alias=by_alias)
        try:
            self.case.assertDictEqual(expected_serialized, result_serialized, msg)
        except AssertionError as error:
            logger.error(
                f"\n - expected: {expected_serialized}"
                f"\n - result  : {result_serialized}"
            )
            raise error

    def assert_list(self, expected: list, result: list, by_alias: bool = False, msg: str = None):
        """ Serialize the lists and check that they are equal """
        expected_serialized = self.serialize_data(data=expected, by_alias=by_alias)
        result_serialized = self.serialize_data(data=result, by_alias=by_alias)
        try:
            self.case.assertListEqual(expected_serialized, result_serialized, msg)
        except AssertionError as error:
            logger.error(
                f"\n - expected: {expected_serialized}"
                f"\n - result  : {result_serialized}"
            )
            raise error

    def assert_dict_diff(
            self, expected: dict or BaseModel, result: dict or BaseModel, by_alias: bool = False, msg: str = None
    ):
        """ Serialize the dictionaries and check that they are not equal """
        with pytest.raises(AssertionError):
            self.assert_dict(expected=expected, result=result, by_alias=by_alias, msg=msg)
            assert True

    def assert_list_diff(self, expected: list, result: list, by_alias: bool = False, msg: str = None):
        """ Serialize the list and check that they are not equal """
        with pytest.raises(AssertionError):
            self.assert_list(expected=expected, result=result, by_alias=by_alias, msg=msg)
            assert True

    # -------------------------------------------------------------------------------------------
    # --- Useful methods of accessing files in the data directory
    # -------------------------------------------------------------------------------------------

    @classmethod
    def join_params(cls, params: List[Any] = None) -> str:
        """
        Returns a string with the union of the parameters
            <param1>..._<param_n>_request.json
        """
        return '_'.join(list(map(lambda p: str(p).replace('.', '').lower(), params))) if params else ''

    def compose_test_file_name(self, file_name: str = None, params: List[Any] = None, extension: str = "json") -> str:
        """
        Returns a file name that begins with the value indicated in "file_name" or with the name of the test run,
        followed by the union of the parameters and the concatenation of the extension
            <test_method_name>_<param1>..._<param_n>_request.json
        """
        return f"{file_name or self.method}{f'_{self.join_params(params=params)}' if params else ''}.{extension}"

    def compose_test_file_path(
            self, data_dir: Path = None, file_name: str = None, params: List[Any] = None, data_type: str = '',
            extension: str = "json"
    ) -> str:
        """
        Returns the path to the file stored in the directory specified by "data_dir", and
        whose name begins with the value indicated in "file_name" or with the name of the test run,
        followed by the union of the parameters and the concatenation of the extension
            data_dir/<test_method_name>_<param1>..._<param_n>_request.json
        """
        _data_type = [data_type] if data_type else []
        return str((data_dir or self._data_path).joinpath(
            self.compose_test_file_name(file_name=file_name, params=(params or []) + _data_type, extension=extension)))

    # -------------------------------------------------------------------------------------------

    def get_data_path(
            self, data_path: Path = None, file_name: str = None, params: List[Any] = None
    ) -> dict or list:
        """ Returns the content of the JSON file with the values used in the test """
        return read_json(file_path=self.compose_test_file_path(data_dir=data_path, file_name=file_name, params=params))

    def get_data_path_input(
            self, data_path: Path = None, file_name: str = None, params: List[Any] = None
    ) -> dict or list:
        """ Returns the content of the JSON file with the input values used in the test """
        return read_json(file_path=self.compose_test_file_path(
            data_dir=data_path, file_name=file_name, params=params, data_type='in'))

    def get_data_path_output(
            self, data_path: Path = None, file_name: str = None, params: List[Any] = None
    ) -> dict or list:
        """ Returns the content of the JSON file with the output values expected to be obtained in the test """
        return read_json(file_path=self.compose_test_file_path(
            data_dir=data_path, file_name=file_name, params=params, data_type='out'))
