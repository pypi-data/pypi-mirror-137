import unittest
from pathlib import Path

import pandas as pd

from model_quality_report.splitters.temporal.time_delta import TimeDeltaDataSplitter


class TestTimeDeltaDataSplitter(unittest.TestCase):
    def setUp(self):
        data_path = Path(__file__).parent.parent.parent / "data" / "date-value_df.pkl"
        test_data = pd.read_pickle(data_path)
        self.X = test_data.loc[:, ["date"]]
        self.X["date"] = pd.to_datetime(self.X["date"])
        self.y = test_data["value"]

    def test_splits_according_last_x_days(self):
        magnitude = 30
        unit = "D"

        splitter = TimeDeltaDataSplitter(date_column_name="date", time_delta=pd.Timedelta(magnitude, unit=unit))

        X_train, X_test, y_train, y_test = splitter.split(self.X, self.y)[0]

        self.assertGreaterEqual(
            X_test[splitter.date_column_name].min(),
            self.X[splitter.date_column_name].max() - pd.to_timedelta(arg=magnitude, unit=unit),
        )

        self.assertLessEqual(
            X_train[splitter.date_column_name].max(),
            self.X[splitter.date_column_name].max() - pd.to_timedelta(arg=magnitude + 1, unit=unit),
        )

        self.assertSequenceEqual(list(X_train.index), list(y_train.index))
        self.assertSequenceEqual(list(X_test.index), list(y_test.index))

    def test_returns_error_if_time_delta_is_too_large(self):
        splitter = TimeDeltaDataSplitter("date", pd.Timedelta(10000, "D"))
        errors = splitter.validate_parameters(self.X, self.y)

        self.assertTrue(len(errors) > 0)
        self.assertTrue("too large" in errors[0])

    def test_returns_error_if_wrong_time_delta_is_provided(self):
        splitter = TimeDeltaDataSplitter("date", "not_a_time_delta")
        errors = splitter.validate_parameters(self.X, self.y)

        self.assertTrue(len(errors) > 0)
        self.assertTrue("Timedelta" in errors[0])

    def test_parameters_can_be_accessed_by_get_parameters(self):
        time_delta = pd.Timedelta(10000, "D")
        splitter = TimeDeltaDataSplitter("date", time_delta)

        parameters = splitter.get_parameters()

        self.assertIsInstance(parameters, dict)
        self.assertDictEqual(
            {
                TimeDeltaDataSplitter.lbl_date_column_name: "date",
                TimeDeltaDataSplitter.lbl_time_delta: time_delta,
            },
            parameters,
        )

    def test_returns_proper_error_in_case_wrong_data_column_name_is_provided(self):
        not_existing_date_column = "not_existing_date_column"

        splitter = TimeDeltaDataSplitter(not_existing_date_column, pd.Timedelta(10, "D"))
        errors = splitter.validate_parameters(self.X, self.y)

        self.assertTrue(len(errors) > 0)
        self.assertTrue("not_existing_date_column" in errors[0])
