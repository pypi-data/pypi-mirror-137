from typing import List

import pandas as pd

from model_quality_report.splitters.base import SplitterBase, Split, SplitGenerator


class ByHorizon(SplitterBase):
    """
    Produces a list of splits of temporal data such that specific number of observations
    after the specified date is used as test data until the input data is exhausted.

    This class can be of use in Time Series analysis, where one wants to produce predictions for several steps ahead
    starting at different dates, in order to assess predictive power of a model by averaging errors across these dates
    for each specific maximum_horizon.

    The data used by this splitter has to have `pd.DatetimeIndex` as its index and it has to be sorted along this index.

    Example
    -------
    import pandas as pd
    from model_quality_report.splitters.temporal.cross_validation.by_horizon import ByHorizon

    lbl_date = 'date'
    dates = pd.Index(pd.date_range('2019-01-01', periods=6), name=lbl_date)
    X = pd.DataFrame({'a': [1, 2, 4, 5, 7, 20],
                      'b': [3, 5, 7, 10, 15, 30]},
                      index=dates)
    y = pd.Series([3, 6, 8, 10, 12, 30], index=dates)
    splitter = ByHorizon(start_split_date=dates[2], maximum_horizon=2)
    print(splitter.split(X, y))

    [(          a  b
    date
    2019-01-01  1  3
    2019-01-02  2  5,

                a   b
    date
    2019-01-03  4   7
    2019-01-04  5  10,

    date
    2019-01-01    3
    2019-01-02    6
    Freq: D, dtype: int64,

    date
    2019-01-03     8
    2019-01-04    10
    Freq: D, dtype: int64),

    (           a  b
    date
    2019-01-01  1  3
    2019-01-02  2  5
    2019-01-03  4  7,

                a   b
    date
    2019-01-04  5  10
    2019-01-05  7  15,

    date
    2019-01-01    3
    2019-01-02    6
    2019-01-03    8
    Freq: D, dtype: int64,

    date
    2019-01-04    10
    2019-01-05    12
    Freq: D, dtype: int64)]

    """

    lbl_date_column_name = "date_column_name"
    lbl_start_split_date = "start_split_date"
    lbl_split_dates = "split_dates"
    lbl_maximum_horizon = "maximum_horizon"

    def __init__(self, start_split_date: pd.Timestamp, maximum_horizon: int) -> None:
        self.start_split_date = start_split_date
        self.maximum_horizon = maximum_horizon

    def split(self, X: pd.DataFrame, y: pd.Series) -> SplitGenerator:
        """
        Given df with features X, target series y and test config, data are split into test and training data
        taking data from last time_delta long period as test data and the rest as training data.

        :param X:
        :param y:
        :return: list of (X_train, X_test, y_train, y_test)
        """
        for split_date in self._get_all_split_dates(X=X):
            date_filter = X.index <= self._get_latest_valid_date_for_test_set(X=X, split_date=split_date)
            yield self._split_date_data(X=X[date_filter], y=y[date_filter], split_date=split_date)

    @staticmethod
    def _split_date_data(X: pd.DataFrame, y: pd.Series, split_date: pd.Timestamp) -> Split:
        X_train = X.loc[X.index < split_date]
        X_test = X.loc[X.index >= split_date]
        y_train = y[X_train.index]
        y_test = y[X_test.index]
        return X_train, X_test, y_train, y_test

    def validate_parameters(self, X: pd.DataFrame, y: pd.Series) -> List:

        validation_error = list()

        if not isinstance(X.index, pd.DatetimeIndex):
            validation_error.append("X index is not DatetimeIndex.")

        if not isinstance(y.index, pd.DatetimeIndex):
            validation_error.append("y index is not DatetimeIndex.")

        try:
            if X.index.max() < self.start_split_date:
                validation_error.append(
                    "start split date {} is larger than max date {}".format(self.start_split_date, X.index.max())
                )
            if X.index.min() > self.start_split_date:
                validation_error.append(
                    "start split date {} is smaller than min date {}".format(self.start_split_date, X.index.min())
                )
        except TypeError as e:
            validation_error.append(str(e))

        if not pd.Index(X.index).is_monotonic:
            validation_error.append("data is not temporally sorted")

        try:
            if len(X.index > self.start_split_date) < self.maximum_horizon:
                validation_error.append(
                    "maximum_horizon is larger than the number of observations after start_split_date"
                )
        except TypeError as e:
            validation_error.append(str(e))

        return validation_error

    def get_parameters(self) -> dict:
        return {
            self.lbl_start_split_date: self.start_split_date,
            self.lbl_maximum_horizon: self.maximum_horizon,
        }

    def _get_all_split_dates(self, X: pd.DataFrame) -> list:
        return X.loc[self.start_split_date :].iloc[: -self.maximum_horizon].index.to_list()

    def _get_latest_valid_date_for_test_set(self, X: pd.DataFrame, split_date: pd.Timestamp) -> pd.Timestamp:
        return X.loc[split_date:].iloc[: self.maximum_horizon].index.max()
