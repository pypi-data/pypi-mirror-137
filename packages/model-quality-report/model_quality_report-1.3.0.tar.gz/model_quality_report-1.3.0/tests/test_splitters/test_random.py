import unittest

import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal

from model_quality_report.splitters.random import RandomDataSplitter


class TestRandomDataSplitter(unittest.TestCase):
    def test_data_are_split_randomly(self):

        X = pd.DataFrame({"a": [1, 2, 3, 4, 5], "b": ["a", "b", "c", "d", "e"]})
        y = pd.Series(data=range(5))

        splitter = RandomDataSplitter(test_size=0.33, random_state=2)
        X_train, X_test, y_train, y_test = splitter.split(X, y)[0]

        assert_frame_equal(
            X_train,
            pd.DataFrame({"a": [2, 4, 1], "b": ["b", "d", "a"]}, index=[1, 3, 0]),
        )
        assert_frame_equal(X_test, pd.DataFrame({"a": [3, 5], "b": ["c", "e"]}, index=[2, 4]))
        assert_series_equal(y_train, pd.Series([1, 3, 0], index=[1, 3, 0]))
        assert_series_equal(y_test, pd.Series([2, 4], index=[2, 4]))

    def test_error_is_returned_if_test_size_is_too_large(self):
        X = pd.DataFrame({"a": [1, 2, 3, 4, 5], "b": ["a", "b", "c", "d", "e"]})
        y = pd.Series(data=range(5))

        splitter = RandomDataSplitter(test_size=100, random_state=2)

        errors = splitter.validate_parameters(X, y)

        self.assertTrue(len(errors) > 0)
        self.assertTrue("test_size=100" in errors[0])

    def test_parameters_can_be_accessed_by_get_parameters(self):
        splitter = RandomDataSplitter(test_size=100, random_state=2)

        parameters = splitter.get_parameters()

        self.assertIsInstance(parameters, dict)
        self.assertDictEqual({"test_size": 100, "random_state": 2}, parameters)
