"""
This module aims to implement the tests of the "AppConf" class.
"""
# ────────────────────────────────────────── imports ────────────────────────────────────────── #
import pytest

from mlflow_custom_serving.conf.app_conf import AppConf, app_conf_factory

from tests_mlflow_custom_serving.base.base_test import BaseTest
from tests_mlflow_custom_serving.conftest import TESTS_ENV_PATH


# ───────────────────────────────────────────────────────────────────────────────────────────── #
#                                         Test Class                                            #
# ───────────────────────────────────────────────────────────────────────────────────────────── #

class TestAppConf(BaseTest):
    """
    AppConf testing class
    """

    def test_default_app_conf(self):
        """
        Validation of default APP configuration
        """
        conf = AppConf('.unknown')
        expected = dict(
            app_env=None, app_group='turintech', app_name='mlflow_custom_serving',
            app_version='0.0.0', app_id=None)
        self.case.assertDictEqual(expected, conf.dict())

    def test_env_app_conf(self):
        """
        Validation APP configuration loaded from .env.test file
        """
        conf = AppConf(TESTS_ENV_PATH)
        expected = dict(
            app_env='TST', app_group='turintech', app_name='mlflow_custom_serving-test', app_version='vTest',
            app_id='turintech-mlflow_custom_serving-test-TST')
        self.case.assertDictEqual(expected, conf.dict())

    def test_app_conf_factory(self):
        """
        Validation of the app_conf.app_conf_factory method
        """
        defaults = dict(app_env='TST', app_version='vTest')
        conf = app_conf_factory(_env_file=TESTS_ENV_PATH, prefix="TEST", defaults=defaults)
        expected = dict(
            app_env='TST', app_group='turintech-test', app_name='mlflow_custom_serving', app_version='vTest', app_id=None)
        self.case.assertDictEqual(expected, conf.dict())


# ───────────────────────────────────────────────────────────────────────────────────────────── #

if __name__ == "__main__":
    pytest.main()
