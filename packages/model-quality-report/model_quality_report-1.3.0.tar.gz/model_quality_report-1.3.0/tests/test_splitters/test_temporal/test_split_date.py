import unittest
from pathlib import Path

import pandas as pd

from model_quality_report.splitters.temporal.split_date import SplitDateDataSplitter


class TestSplitDateDataSplitter(unittest.TestCase):
    def setUp(self):
        data_path = Path(__file__).parent.parent.parent / "data" / "date-value_df.pkl"
        test_data = pd.read_pickle(data_path)
        self.X = test_data.loc[:, ["date"]]
        self.X["date"] = pd.to_datetime(self.X["date"])
        self.y = test_data["value"]

    def test_splits_according_last_split_date(self):
        split_date = pd.Timestamp("2017-01-01")
        splitter = SplitDateDataSplitter(date_column_name="date", split_date=split_date)

        X_train, X_test, y_train, y_test = splitter.split(self.X, self.y)[0]

        self.assertGreaterEqual(X_test[splitter.date_column_name].min(), split_date)

        self.assertLessEqual(X_train[splitter.date_column_name].max(), split_date)

        self.assertSequenceEqual(list(X_train.index), list(y_train.index))
        self.assertSequenceEqual(list(X_test.index), list(y_test.index))

    def test_returns_error_if_split_date_too_large(self):
        split_date = pd.Timestamp("2100-01-01")
        splitter = SplitDateDataSplitter("date", split_date)
        errors = splitter.validate_parameters(self.X, self.y)

        self.assertTrue(len(errors) > 0)
        self.assertTrue(str(split_date) in errors[0])

    def test_returns_error_if_split_date_too_small(self):
        split_date = pd.Timestamp("1900-01-01")
        splitter = SplitDateDataSplitter("date", split_date)
        errors = splitter.validate_parameters(self.X, self.y)

        self.assertTrue(len(errors) > 0)
        self.assertTrue(str(split_date) in errors[0])

    def test_returns_error_if_wrong_timestamp_is_provided(self):
        splitter = SplitDateDataSplitter("date", "not_a_timestamp")
        errors = splitter.validate_parameters(self.X, self.y)

        self.assertTrue(len(errors) > 0)
        self.assertTrue("Timestamp" in errors[0])

    def test_parameters_can_be_accessed_by_get_parameters(self):
        split_date = pd.Timestamp("1900-01-01")

        splitter = SplitDateDataSplitter("date", split_date)

        parameters = splitter.get_parameters()

        self.assertIsInstance(parameters, dict)
        self.assertDictEqual(
            {
                SplitDateDataSplitter.lbl_date_column_name: "date",
                SplitDateDataSplitter.lbl_split_date: split_date,
            },
            parameters,
        )

    def test_returns_proper_error_in_case_wrong_data_column_name_is_provided(self):
        not_existing_date_column = "not_existing_date_column"

        splitter = SplitDateDataSplitter(not_existing_date_column, pd.Timestamp("1900-01-01"))
        errors = splitter.validate_parameters(self.X, self.y)

        self.assertTrue(len(errors) > 0)
        self.assertTrue("not_existing_date_column" in errors[0])
