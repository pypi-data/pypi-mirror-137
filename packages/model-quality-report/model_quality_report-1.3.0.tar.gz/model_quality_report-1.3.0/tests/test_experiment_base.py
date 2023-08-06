import unittest

import pandas as pd

from tests.linear_model_experiment import LinearModelExperiment


class TestCrossValidationModelComparisonReport(unittest.TestCase):
    def setUp(self):
        dates = pd.date_range("2019-01-01", periods=8)
        index = pd.DatetimeIndex(dates, name="date")
        self.X = pd.DataFrame(
            {
                "a": [1, 2, 4, 5, 7, 20, 6, 11],
                "b": [3, 5, 7, 10, 15, 30, 22, 48],
                "c": [8, 1, 0, 17, 11, 20, 2, 4],
            },
            index=index,
        )
        self.y_data = pd.Series([3, 6, 8, 10, 12, 30, 23, 5], name="y1", index=index)

    def test_experiment_init(self):
        exog_cols = ["a", "b"]
        experiment_key = "key1"
        experiment = LinearModelExperiment(
            x_data=self.X, y_data=self.y_data, exog_cols=exog_cols, experiment_key=experiment_key
        )
        self.assertEqual(experiment.get_experiment_key(), {experiment_key: str(exog_cols)})
        pd.testing.assert_frame_equal(experiment.get_x_data(), self.X)
        pd.testing.assert_series_equal(experiment.get_y_data(), self.y_data)
