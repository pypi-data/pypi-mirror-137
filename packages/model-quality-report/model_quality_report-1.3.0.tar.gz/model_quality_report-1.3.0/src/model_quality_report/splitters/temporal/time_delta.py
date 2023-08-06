from typing import List

import pandas as pd

from model_quality_report.splitters.base import SplitterBase, Splits


class TimeDeltaDataSplitter(SplitterBase):
    """
    Splits data such that provided timedelta is used as test data
    """

    lbl_date_column_name = "date_column_name"
    lbl_time_delta = "time_delta"

    def __init__(self, date_column_name: str, time_delta: pd.Timedelta) -> None:
        self.date_column_name = date_column_name
        self.time_delta = time_delta

    def split(self, X: pd.DataFrame, y: pd.Series) -> Splits:
        """
        Given df with features X, target series y, data are split into test and training data
        taking data from last time_delta long period as test data and the rest as training data.
        :param X:
        :param y:
        :return: X_train, X_test, y_train, y_test
        """
        split_date = X[self.date_column_name].max() - self.time_delta
        X_train = X[X[self.date_column_name] < split_date]
        X_test = X[X[self.date_column_name] >= split_date]
        y_train = y[X_train.index]
        y_test = y[X_test.index]
        return [(X_train, X_test, y_train, y_test)]

    def validate_parameters(self, X: pd.DataFrame, y: pd.Series) -> List:
        validation_error = list()

        try:
            X[self.date_column_name]
        except KeyError as e:
            validation_error.append("Column {} does not exist in DataFrame X".format(e))
            return validation_error

        try:
            if (X[self.date_column_name].max() - X[self.date_column_name].min()) < self.time_delta:
                validation_error.append("time_delta {} is too large for data".format(self.time_delta))
        except TypeError as e:
            validation_error.append(str(e))

        return validation_error

    def get_parameters(self):
        return {
            self.lbl_date_column_name: self.date_column_name,
            self.lbl_time_delta: self.time_delta,
        }
