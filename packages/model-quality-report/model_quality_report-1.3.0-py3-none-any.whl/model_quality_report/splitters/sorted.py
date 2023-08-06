from typing import List

import pandas as pd

from model_quality_report.splitters.base import SplitterBase, Splits


class SortedDataSplitter(SplitterBase):
    """
    Splits data after sorting along a given column such that last test_size data are used as test_data. Thereby,
    test_size must be larger than 0 and smaller than 1.
    """

    lbl_sortable_column_name = "sortable_column_name"
    lbl_test_size = "test_size"
    lbl_ascending = "ascending"

    def __init__(self, sortable_column_name: str, test_size: float, ascending: bool = True) -> None:
        self.sortable_column_name = sortable_column_name
        self.test_size = test_size
        self.ascending = ascending

    def split(self, X: pd.DataFrame, y: pd.Series) -> Splits:
        """
        Given df with features X, target series y data are split into test and training data
        such that
        :param X:
        :param y:
        :return: X_train, X_test, y_train, y_test
        """
        X = X.sort_values(by=self.sortable_column_name, ascending=self.ascending)
        X_train = X.iloc[: int((1 - self.test_size) * X.shape[0])]
        X_test = X.iloc[int((1 - self.test_size) * X.shape[0]) :]
        y_train = y[X_train.index]
        y_test = y[X_test.index]
        return [(X_train, X_test, y_train, y_test)]

    def validate_parameters(self, X: pd.DataFrame, y: pd.Series) -> List:
        validation_error = list()

        try:
            X[self.sortable_column_name]
        except KeyError as e:
            validation_error.append("Column {} does not exist in DataFrame X".format(e))
            return validation_error

        try:
            X.sort_values(by=self.sortable_column_name)
        except TypeError as e:
            validation_error.append(str(e))

        if (self.test_size < 0) | (self.test_size > 1):
            validation_error.append("test_size should be between 0 and 1")

        return validation_error

    def get_parameters(self) -> dict:
        return {
            self.lbl_sortable_column_name: self.sortable_column_name,
            self.lbl_test_size: self.test_size,
            self.lbl_ascending: self.ascending,
        }
