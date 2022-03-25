"""
This module aims to implement the tests of the "formatting_utils" module.
"""
# ────────────────────────────────────────── imports ────────────────────────────────────────── #
import pytest

from mlflow_custom_serving.utils.formatting_utils import get_start_end, get_list_formatter, get_dict_formatter, \
    get_data_formatter

from tests_mlflow_custom_serving.base.base_test import BaseTest


# ───────────────────────────────────────────────────────────────────────────────────────────── #
#                                         Test Class                                            #
# ───────────────────────────────────────────────────────────────────────────────────────────── #

class TestFormattingUtils(BaseTest):
    """
    Formatting Utils testing class
    """

    def test_get_start_end(self):
        """
        It validates that the expected format is obtained to represent a group of data.
        """

        title = "test_get_start_end"
        print_char = "="
        size = 90
        expected_start = "=================================== test_get_start_end ==================================="
        expected_end = print_char * size

        start, end = get_start_end(title=title, print_char=print_char, size=size, nl_str=True, nl_end=False)
        self.case.assertEqual(f"\n{expected_start}", start, "Header of group with NL")
        self.case.assertEqual(expected_end, end, "Footer of group without NL")

        start, end = get_start_end(title=title, print_char=print_char, size=size, nl_str=False, nl_end=True)
        self.case.assertEqual(expected_start, start, "Header of group with out NL")
        self.case.assertEqual(f"{expected_end}\n", end, "Footer of group with NL")

    def test_get_list_formatter_simple(self):
        """
        It is validated that the expected format is obtained to represent a list
        """

        title = "test_get_dict_list"
        print_char = "-"
        size = 90

        data = [1, 2, "value1", "value2"]

        expected = "\n    - 1" \
                   "\n    - 2" \
                   "\n    - value1" \
                   "\n    - value2\n"
        result = get_list_formatter(data=data, indent=1)
        self.case.assertEqual(expected, result, "Simple list")

        expected = "\n    - 1" \
                   "\n    - 2" \
                   "\n    - value1" \
                   "\n    - value2"
        result = get_list_formatter(data=data, indent=1, nl_end=False)
        self.case.assertEqual(expected, result, "Simple list")

        expected = "\n----------------------------------- test_get_dict_list -----------------------------------" \
                   "\n        - 1" \
                   "\n        - 2" \
                   "\n        - value1" \
                   "\n        - value2" \
                   "\n------------------------------------------------------------------------------------------\n"
        result = get_list_formatter(
            data=data, indent=2, title=title, print_char=print_char, size=size, nl_str=True, nl_end=True)
        self.case.assertEqual(expected, result, "Simple list with title")

    def test_get_dict_formatter_simple(self):
        """
        It is validated that the expected format is obtained to represent a dictionary
        """

        title = "test_get_dict_formatter"
        print_char = "-"
        size = 90

        data = dict(key1=1, key2="value2")
        expected = "\n-------------------------------- test_get_dict_formatter --------------------------------" \
                   "\n    - key1 : 1" \
                   "\n    - key2 : value2" \
                   "\n-----------------------------------------------------------------------------------------\n"
        result = get_dict_formatter(data=data, title=title, print_char=print_char, size=size, nl_str=True, nl_end=True)
        self.case.assertEqual(expected, result, "Simple dict")

    def test_get_data_formatter_1(self):
        """
        This method validates the formatting_utils.get_data_formatter method
        """
        title = self.method
        print_char = "-"
        size = 90
        data = dict(
            val1=[1, 2, 3], val2=dict(key1=3, key2="value2", key3=[dict(k1=1, k2=2, k3=[5, 43, 2]), [1, 2, 3, 4]]))
        expected = f"\n------------------------------- {title} -------------------------------" \
                   "\n    - val1 : [1, 2, 3]" \
                   "\n    - val2 : {'key1': 3, 'key2': 'value2', " \
                   "'key3': [{'k1': 1, 'k2': 2, 'k3': [5, 43, 2]}, [1, 2, 3, 4]]}" \
                   "\n-----------------------------------------------------------------------------------------\n"

        result = get_data_formatter(
            data=data, title=title, print_char=print_char, size=size, nl_str=True, nl_end=True, levels=1)
        self.case.assertEqual(expected, result)

    def test_get_data_formatter_2(self):
        """
        This method validates the formatting_utils.get_data_formatter method
        """
        title = self.method
        print_char = "-"
        size = 90
        data = dict(
            val1=[1, 2, 3], val2=dict(key1=3, key2="value2", key3=[dict(k1=1, k2=2, k3=[5, 43, 2]), [1, 2, 3, 4]]))
        expected = f"\n------------------------------- {title} -------------------------------" \
                   "\n    - val1 : " \
                   "\n        - 1" \
                   "\n        - 2" \
                   "\n        - 3" \
                   "\n    - val2 : " \
                   "\n        - key1 : 3" \
                   "\n        - key2 : value2" \
                   "\n        - key3 : [{'k1': 1, 'k2': 2, 'k3': [5, 43, 2]}, [1, 2, 3, 4]]" \
                   "\n-----------------------------------------------------------------------------------------\n"

        result = get_data_formatter(
            data=data, title=title, print_char=print_char, size=size, nl_str=True, nl_end=True, levels=2)
        self.case.assertEqual(expected, result)

    def test_get_data_formatter_3(self):
        """
        This method validates the formatting_utils.get_data_formatter method
        """
        title = self.method
        print_char = "-"
        size = 90
        data = dict(
            val1=[1, 2, 3], val2=dict(key1=3, key2="value2", key3=[dict(k1=1, k2=2, k3=[5, 43, 2]), [1, 2, 3, 4]]))
        expected = f"\n------------------------------- {title} -------------------------------" \
                   "\n    - val1 : " \
                   "\n        - 1" \
                   "\n        - 2" \
                   "\n        - 3" \
                   "\n    - val2 : " \
                   "\n        - key1 : 3" \
                   "\n        - key2 : value2" \
                   "\n        - key3 : " \
                   "\n            - k1 : 1" \
                   "\n            - k2 : 2" \
                   "\n            - k3 : [5, 43, 2]" \
                   "\n            - 1" \
                   "\n            - 2" \
                   "\n            - 3" \
                   "\n            - 4" \
                   "\n-----------------------------------------------------------------------------------------\n"
        result = get_data_formatter(
            data=data, title=title, print_char=print_char, size=size, nl_str=True, nl_end=True, levels=3)
        self.case.assertEqual(expected, result)

    def test_get_data_formatter_4(self):
        """
        This method validates the formatting_utils.get_data_formatter method
        """
        title = self.method
        print_char = "-"
        size = 90
        data = dict(
            val1=[1, 2, 3], val2=dict(key1=3, key2="value2", key3=[dict(k1=1, k2=2, k3=[5, 43, 2]), [1, 2, 3, 4]]))
        expected = f"\n------------------------------- {title} -------------------------------" \
                   "\n    - val1 : " \
                   "\n        - 1" \
                   "\n        - 2" \
                   "\n        - 3" \
                   "\n    - val2 : " \
                   "\n        - key1 : 3" \
                   "\n        - key2 : value2" \
                   "\n        - key3 : " \
                   "\n            - k1 : 1" \
                   "\n            - k2 : 2" \
                   "\n            - k3 : " \
                   "\n                - 5" \
                   "\n                - 43" \
                   "\n                - 2" \
                   "\n            - 1" \
                   "\n            - 2" \
                   "\n            - 3" \
                   "\n            - 4" \
                   "\n-----------------------------------------------------------------------------------------\n"

        result = get_data_formatter(
            data=data, title=title, print_char=print_char, size=size, nl_str=True, nl_end=True, levels=4)
        self.case.assertEqual(expected, result)


# ───────────────────────────────────────────────────────────────────────────────────────────── #

if __name__ == "__main__":
    pytest.main()
