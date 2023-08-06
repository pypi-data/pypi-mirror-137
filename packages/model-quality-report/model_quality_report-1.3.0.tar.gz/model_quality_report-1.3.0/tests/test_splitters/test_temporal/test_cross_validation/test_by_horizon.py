import unittest
from pathlib import Path

import pandas as pd

from model_quality_report.splitters.temporal.cross_validation.by_horizon import ByHorizon


class TestByHorizon(unittest.TestCase):
    def setUp(self):
        data_path = Path(__file__).parent.parent.parent.parent / "data" / "date-value_df.pkl"
        test_data = (
            pd.read_pickle(data_path)
            .drop_duplicates(subset=["date"])
            .assign(date=lambda x: pd.to_datetime(x["date"]))
            .set_index("date")
            .sort_index()
        )
        self.X = test_data.assign(date=lambda x: x.index)
        self.y = test_data["value"]

    def test_correct_number_of_splits(self):
        start_split_date = pd.Timestamp("2017-01-01")
        maximum_horizon = 10
        splitter = ByHorizon(start_split_date=start_split_date, maximum_horizon=maximum_horizon)

        splits = list(splitter.split(self.X, self.y))

        self.assertEqual(
            len(splits),
            self.X[self.X["date"] >= start_split_date].shape[0] - maximum_horizon,
        )

    def test_split_date_boundaries(self):
        start_split_date = pd.Timestamp("2017-01-01")
        maximum_horizon = 10
        splitter = ByHorizon(start_split_date=start_split_date, maximum_horizon=maximum_horizon)

        splits = splitter.split(self.X, self.y)

        for X_train, X_test, y_train, y_test in splits:
            self.assertGreaterEqual(X_test.index.min(), start_split_date)
            self.assertLess(X_train.index.max(), X_test.index.min())

    def test_equality_of_split_x_an_y_indices(self):
        start_split_date = pd.Timestamp("2017-01-01")
        maximum_horizon = 10
        splitter = ByHorizon(start_split_date=start_split_date, maximum_horizon=maximum_horizon)

        splits = splitter.split(self.X, self.y)

        for X_train, X_test, y_train, y_test in splits:
            self.assertSequenceEqual(list(X_train.index), list(y_train.index))
            self.assertSequenceEqual(list(X_test.index), list(y_test.index))

    def test_length_of_test_data(self):
        start_split_date = pd.Timestamp("2017-01-01")
        maximum_horizon = 10
        splitter = ByHorizon(start_split_date=start_split_date, maximum_horizon=maximum_horizon)

        splits = splitter.split(self.X, self.y)

        for X_train, X_test, y_train, y_test in splits:
            self.assertEqual(X_test.shape[0], maximum_horizon)
            self.assertEqual(y_test.shape[0], maximum_horizon)

    def test_increment_of_train_data(self):
        start_split_date = pd.Timestamp("2017-01-01")
        maximum_horizon = 10
        splitter = ByHorizon(start_split_date=start_split_date, maximum_horizon=maximum_horizon)

        splits = list(splitter.split(self.X, self.y))

        for split, split_next in zip(splits[:-1], splits[1:]):
            X_train, _, y_train, _ = split
            X_train_next, _, y_train_next, _ = split_next
            self.assertEqual(X_train.shape[0], X_train_next.shape[0] - 1)
            self.assertEqual(y_train.shape[0], y_train_next.shape[0] - 1)

    def test_returns_error_if_no_datetime_index(self):
        start_split_date = pd.Timestamp("2017-01-01")
        maximum_horizon = 10
        splitter = ByHorizon(start_split_date=start_split_date, maximum_horizon=maximum_horizon)
        errors = splitter.validate_parameters(self.X.reset_index(drop=True), self.y)

        self.assertTrue(len(errors) > 0)
        self.assertTrue("DatetimeIndex" in errors[0])

        errors = splitter.validate_parameters(self.X, self.y.reset_index(drop=True))

        self.assertTrue(len(errors) > 0)
        self.assertTrue("DatetimeIndex" in errors[0])

    def test_returns_error_if_split_date_too_large(self):
        start_split_date = pd.Timestamp("2100-01-01")
        maximum_horizon = 10
        splitter = ByHorizon(start_split_date=start_split_date, maximum_horizon=maximum_horizon)

        errors = splitter.validate_parameters(self.X, self.y)

        self.assertTrue(len(errors) > 0)
        self.assertTrue(str(start_split_date) in errors[0])

    def test_returns_error_if_split_date_too_small(self):
        start_split_date = pd.Timestamp("1900-01-01")
        maximum_horizon = 10
        splitter = ByHorizon(start_split_date=start_split_date, maximum_horizon=maximum_horizon)

        errors = splitter.validate_parameters(self.X, self.y)

        self.assertTrue(len(errors) > 0)
        self.assertTrue(str(start_split_date) in errors[0])

    def test_returns_error_if_maximum_horizon_too_large(self):
        start_split_date = pd.Timestamp("2017-01-01")
        maximum_horizon = 1000
        splitter = ByHorizon(start_split_date=start_split_date, maximum_horizon=maximum_horizon)

        errors = splitter.validate_parameters(self.X, self.y)

        self.assertTrue(len(errors) > 0)
        self.assertTrue("maximum_horizon" in errors[0])

    def test_returns_error_if_wrong_timestamp_is_provided(self):
        splitter = ByHorizon(start_split_date="not_a_timestamp", maximum_horizon=10)
        errors = splitter.validate_parameters(self.X, self.y)

        self.assertTrue(len(errors) > 0)
        self.assertTrue("Timestamp" in errors[0])

    def test_parameters_can_be_accessed_by_get_parameters(self):
        start_split_date = pd.Timestamp("1900-01-01")
        maximum_horizon = 10

        splitter = ByHorizon(start_split_date=start_split_date, maximum_horizon=maximum_horizon)

        parameters = splitter.get_parameters()

        self.assertIsInstance(parameters, dict)
        self.assertDictEqual(
            {
                ByHorizon.lbl_start_split_date: start_split_date,
                ByHorizon.lbl_maximum_horizon: maximum_horizon,
            },
            parameters,
        )
