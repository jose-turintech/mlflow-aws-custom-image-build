"""
This module aims to implement the tests of the "ConfManager" singleton class.
"""
# pylint: disable=W0212
#       W0212: Access to a protected member _logging_conf of a client class (protected-access)
# ────────────────────────────────────────── imports ────────────────────────────────────────── #
import pytest

from mlflow_custom_serving.conf.conf_manager import conf_mgr, ConfManager
from mlflow_custom_serving.conf.data_conf import DataConf
from mlflow_custom_serving.conf.logger_conf import FileLoggerConf

from tests_mlflow_custom_serving.base.base_test import BaseTest
from tests_mlflow_custom_serving.conftest import ROOT_PATH, TESTS_ENV_PATH, data_mgr


# ───────────────────────────────────────────────────────────────────────────────────────────── #
#                                         Test Class                                            #
# ───────────────────────────────────────────────────────────────────────────────────────────── #

class TestConfManager(BaseTest):
    """
    Configuration Manager testing class
    """

    def test_init(self):
        """
        Validation of the ConfManager.__init__
        """
        conf1 = ConfManager()
        conf2 = ConfManager(env_file=TESTS_ENV_PATH)

        self.case.assertEqual(str(ROOT_PATH.joinpath(*['deploy', '.env'])), conf1.env_file)
        self.case.assertEqual(str(TESTS_ENV_PATH), conf2.env_file)

    def test_update_conf_mgr(self):
        """
        Validation of the ConfManager.update_conf_mgr
        """
        conf = ConfManager()
        self.case.assertEqual(str(ROOT_PATH.joinpath(*['deploy', '.env'])), conf.env_file)

        conf.update_conf_mgr(env_file=str(TESTS_ENV_PATH))
        self.case.assertEqual(str(TESTS_ENV_PATH), conf.env_file)

        conf.update_conf_mgr(env_file='.env')
        self.case.assertIsNone(conf.env_file)

    def test_app_paths(self):
        """
        Validation of the ConfManager path configurations
        """
        expected = ROOT_PATH
        self.case.assertEqual(expected, conf_mgr.path_root, "path_root")

        expected = ROOT_PATH.joinpath('deploy')
        self.case.assertEqual(expected, conf_mgr.path_deploy, "path_deploy")

        expected = ROOT_PATH.joinpath('src')
        self.case.assertEqual(expected, conf_mgr.path_src, "path_src")

        expected = expected.joinpath('mlflow_custom_serving')
        self.case.assertEqual(expected, conf_mgr.path_app, "path_app")

        expected = expected.joinpath('conf')
        self.case.assertEqual(expected, conf_mgr.path_conf, "path_conf")

    def test_logging_conf(self):
        """
        Validation of the logging_conf property
        """
        expected = FileLoggerConf(_env_file=TESTS_ENV_PATH, sink=conf_mgr.defaults_logging_conf.get('sink'),
                                  level="debug", defaults=dict(unknown="unknown")).dict()
        self.case.assertDictEqual(expected, conf_mgr.logging_conf.dict())

        conf_mgr._logging_conf = None
        self.case.assertDictEqual(expected, conf_mgr.logging_conf.dict())

    def test_data_conf(self):
        """
        Validation of the data_conf property
        """
        expected = DataConf(_env_file=TESTS_ENV_PATH, data_path=data_mgr.data_path,
                            defaults=dict(unknown="unknown")).dict()
        self.case.assertDictEqual(expected, conf_mgr.data_conf.dict())

        conf_mgr._data_conf = None
        self.case.assertDictEqual(expected, conf_mgr.data_conf.dict())


# ───────────────────────────────────────────────────────────────────────────────────────────── #

if __name__ == "__main__":
    pytest.main()
