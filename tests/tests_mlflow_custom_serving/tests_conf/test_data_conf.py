"""
This module aims to implement the tests of the "DataConf" class.
"""
# ────────────────────────────────────────── imports ────────────────────────────────────────── #
from pathlib import Path

import pytest
from pydantic import ValidationError

from mlflow_custom_serving.conf.data_conf import DataConf, data_conf_factory

from tests_mlflow_custom_serving.base.base_test import BaseTest
from tests_mlflow_custom_serving.conftest import TESTS_ENV_PATH


# ───────────────────────────────────────────────────────────────────────────────────────────── #
#                                         Test Class                                            #
# ───────────────────────────────────────────────────────────────────────────────────────────── #

class TestDataConf(BaseTest):
    """
    DataConf testing class
    """

    def test_default_data_conf(self):
        """
        Validation of default APP configuration
        """
        expected = "1 validation error for DataConf\n" \
                   "data_path\n  field required (type=value_error.missing)"
        with pytest.raises(ValidationError) as error:
            DataConf()
        self.case.assertEqual(expected, str(error.value), "1 ValidationError")

    def test_env_data_conf(self):
        """
        Validation APP configuration loaded from .env.test file
        """
        conf = DataConf(_env_file=TESTS_ENV_PATH, data_path="./data")
        expected = dict(data_path=Path("./data").resolve())
        self.case.assertDictEqual(expected, conf.dict())

    def test_data_conf_factory(self):
        """
        Validation of the app_conf.app_conf_factory method
        """
        defaults = dict(data_path="./data")
        conf = data_conf_factory(_env_file=TESTS_ENV_PATH, prefix="TEST", defaults=defaults)
        expected = dict(data_path=Path("./data").resolve())
        self.case.assertDictEqual(expected, conf.dict())


# ───────────────────────────────────────────────────────────────────────────────────────────── #

if __name__ == "__main__":
    pytest.main()
