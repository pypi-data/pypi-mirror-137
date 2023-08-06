from typing import List

import pandas as pd

from model_quality_report.splitters.base import SplitterBase, Splits


class SplitDateDataSplitter(SplitterBase):
    """
    Splits data such that the data after provided split_date is used as test data
    """

    lbl_date_column_name = "date_column_name"
    lbl_split_date = "split_date"

    def __init__(self, date_column_name: str, split_date: pd.Timestamp) -> None:
        self.date_column_name = date_column_name
        self.split_date = split_date

    def split(self, X: pd.DataFrame, y: pd.Series) -> Splits:
        """
        Given df with features X, target series y and test config, data are split into test and training data
        taking data from last time_delta long period as test data and the rest as training data.
        :param X:
        :param y:
        :return: X_train, X_test, y_train, y_test
        """

        X_train = X[X[self.date_column_name] < self.split_date]
        X_test = X[X[self.date_column_name] >= self.split_date]
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
            if X[self.date_column_name].max() < self.split_date:
                validation_error.append(
                    "split date {} is larger than max date {}".format(self.split_date, X[self.date_column_name].max())
                )
            if X[self.date_column_name].min() > self.split_date:
                validation_error.append(
                    "split date {} is smaller than min date {}".format(self.split_date, X[self.date_column_name].min())
                )
        except TypeError as e:
            validation_error.append(str(e))

        return validation_error

    def get_parameters(self) -> dict:
        return {
            self.lbl_date_column_name: self.date_column_name,
            self.lbl_split_date: self.split_date,
        }
