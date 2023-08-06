import unittest
from pathlib import Path

import pandas as pd
from numpy.random import randint
from parameterized import parameterized

from model_quality_report.splitters.temporal.cross_validation.fixed_dates import FixedDates


class TestFixedDates(unittest.TestCase):
    def setUp(self):
        data_path = Path(__file__).parent.parent.parent.parent / "data" / "date-value_df.pkl"
        test_data = (
            pd.read_pickle(data_path)
            .drop_duplicates(subset=["date"])
            .assign(date=lambda x: pd.to_datetime(x["date"]))
            .sort_values(by="date")
            .reset_index(drop=True)
        )
        self.X = test_data.assign(**{"exog": lambda x: randint(100, size=test_data.shape[0])}).drop(columns=["value"])
        self.y = test_data.set_index("date")["value"]

    @parameterized.expand([(x,) for x in range(1, 4)])
    def test_correct_number_of_splits(self, periods: int):
        split_dates = pd.date_range(start="2017-01-01", periods=periods)
        splitter = FixedDates(split_dates=split_dates, date_column_name="date")

        splits = list(splitter.split(self.X, self.y))

        self.assertEqual(len(splits), periods)

    @parameterized.expand([(x,) for x in range(1, 4)])
    def test_split_date_boundaries(self, periods: int):
        split_dates = pd.date_range(start="2017-01-01", periods=periods)
        splitter = FixedDates(split_dates=split_dates, date_column_name="date")

        splits = splitter.split(self.X, self.y)

        for start_split_date, (X_train, X_test, y_train, y_test) in zip(split_dates, splits):
            self.assertGreaterEqual(X_test["date"].min(), start_split_date)
            self.assertLess(X_train["date"].max(), X_test["date"].min())
            self.assertGreaterEqual(y_test.index.min(), start_split_date)
            self.assertLess(y_train.index.max(), y_test.index.min())

    @parameterized.expand([(x,) for x in range(1, 4)])
    def test_increment_of_train_data(self, periods: int):
        split_dates = pd.date_range(start="2017-01-01", periods=periods)
        splitter = FixedDates(split_dates=split_dates, date_column_name="date")

        splits = list(splitter.split(self.X, self.y))

        for split, split_next in zip(splits[:-1], splits[1:]):
            X_train, _, y_train, _ = split
            X_train_next, _, y_train_next, _ = split_next
            self.assertLessEqual(X_train.shape[0], X_train_next.shape[0])
            self.assertLessEqual(y_train.shape[0], y_train_next.shape[0])

    @parameterized.expand([(x,) for x in range(1, 4)])
    def test_returns_error_if_no_datetime_index(self, periods: int):
        split_dates = pd.date_range(start="2017-01-01", periods=periods)
        splitter = FixedDates(split_dates=split_dates, date_column_name="date")

        errors = splitter.validate_parameters(self.X, self.y.reset_index(drop=True))

        self.assertTrue(len(errors) > 0)
        self.assertTrue("DatetimeIndex" in errors[0])

    def test_returns_error_if_split_date_too_large(self):
        start_split_date = self.X["date"].max() + pd.DateOffset(days=1)
        split_dates = pd.date_range(start=start_split_date, periods=3)
        splitter = FixedDates(split_dates=split_dates, date_column_name="date")

        errors = splitter.validate_parameters(self.X, self.y)

        self.assertTrue(len(errors) > 0)
        self.assertTrue(str(split_dates.max()) in errors[0])

    def test_returns_error_if_split_date_too_small(self):
        start_split_date = self.X["date"].min() - pd.DateOffset(days=1)
        split_dates = pd.date_range(start=start_split_date, periods=3)
        splitter = FixedDates(split_dates=split_dates, date_column_name="date")

        errors = splitter.validate_parameters(self.X, self.y)

        self.assertTrue(len(errors) > 0)
        self.assertTrue(str(split_dates.min()) in errors[0])

    def test_returns_error_if_wrong_date_col_is_provided(self):
        split_dates = pd.date_range(start="2017-01-01", periods=3)
        splitter = FixedDates(split_dates=split_dates, date_column_name="exog")

        errors = splitter.validate_parameters(self.X, self.y)

        self.assertTrue(len(errors) > 0)
        self.assertTrue("exog" in errors[0])

    def test_returns_error_if_date_col_in_x_is_not_monotonic(self):
        split_dates = pd.date_range(start="2017-01-01", periods=3)
        splitter = FixedDates(split_dates=split_dates, date_column_name="date")

        errors = splitter.validate_parameters(self.X.sample(len(self.X)), self.y)

        self.assertTrue(len(errors) > 0)
        self.assertTrue("sorted" in errors[0])

        errors = splitter.validate_parameters(self.X, self.y)

        self.assertEqual(len(errors), 0)

    def test_returns_error_if_date_col_in_y_is_not_monotonic(self):
        split_dates = pd.date_range(start="2017-01-01", periods=3)
        splitter = FixedDates(split_dates=split_dates, date_column_name="date")

        errors = splitter.validate_parameters(self.X, self.y.sample(len(self.y)))

        self.assertTrue(len(errors) > 0)
        self.assertTrue("sorted" in errors[0])

        errors = splitter.validate_parameters(self.X, self.y)

        self.assertEqual(len(errors), 0)

    def test_parameters_can_be_accessed_by_get_parameters(self):
        split_dates = pd.date_range(start="2017-01-01", periods=3)
        splitter = FixedDates(split_dates=split_dates, date_column_name="date")

        parameters = splitter.get_parameters()

        self.assertIsInstance(parameters, dict)
        self.assertDictEqual(
            {FixedDates.lbl_split_dates: split_dates, FixedDates.lbl_date_column_name: "date"}, parameters
        )
