from typing import List

import pandas as pd
from pandas.core.dtypes.common import is_datetime64_ns_dtype

from model_quality_report.splitters.base import SplitterBase, Split, SplitGenerator


class FixedDates(SplitterBase):
    """
    Produces a list of splits of temporal data given a list of fixed dates.

    This class can be of use in Time Series analysis, where one wants to produce predictions for several steps ahead
    starting at different dates, in order to assess predictive power of a model by averaging errors across these dates
    for each specific horizon.

    The X data used by this splitter has to have a `datetime64[ns]` column, and it has to be sorted along this column.
    The y data used by this splitter has to have `pd.DatetimeIndex` as its index and it has to be sorted along this index.

    Example
    -------
    import pandas as pd
    from model_quality_report.splitters.temporal.cross_validation.fixed_dates import FixedDates

    lbl_date = 'date'
    dates = pd.Index(pd.date_range('2019-01-01', periods=6), name=lbl_date)
    X = pd.DataFrame({'a': [1, 2, 4, 5, 7, 20],
                      'b': [3, 5, 7, 10, 15, 30],
                      lbl_date: dates})
    y = pd.Series([3, 6, 8, 10, 12, 30], index=dates)
    splitter = FixedDates(split_dates=pd.date_range('2019-01-04', periods=3), date_column_name=lbl_date)
    splitter.split(X, y)

    """

    lbl_date_column_name = "date_column_name"
    lbl_split_dates = "split_dates"

    def __init__(self, split_dates: pd.DatetimeIndex, date_column_name: str) -> None:
        self.split_dates = split_dates
        self.date_column_name = date_column_name

    def split(self, X: pd.DataFrame, y: pd.Series) -> SplitGenerator:
        """
        Given df with features X, target series y and test config, data are split into test and training data
        taking data from last time_delta long period as test data and the rest as training data.

        :param X:
        :param y:
        :return: list of (X_train, X_test, y_train, y_test)
        """
        for split_date in self._get_all_split_dates():
            yield self._split_date_data(X=X, y=y, split_date=split_date)

    def _split_date_data(self, X: pd.DataFrame, y: pd.Series, split_date: pd.Timestamp) -> Split:
        X_train = X.loc[X[self.date_column_name] < split_date]
        X_test = X.loc[X[self.date_column_name] >= split_date]
        y_train = y.loc[y.index < split_date]
        y_test = y.loc[y.index >= split_date]
        return X_train, X_test, y_train, y_test

    def validate_parameters(self, X: pd.DataFrame, y: pd.Series) -> List:
        validation_error = list()

        if not isinstance(y.index, pd.DatetimeIndex):
            validation_error.append("y index is not DatetimeIndex.")

        if not is_datetime64_ns_dtype(X[self.date_column_name]):
            validation_error.append(f"{self.date_column_name} column is not datetime64[ns].")

        try:
            if X[self.date_column_name].max() < self.split_dates.max():
                validation_error.append(
                    f"max split date {self.split_dates.max()} is larger "
                    f"than max date in the data {X[self.date_column_name].max()}"
                )
            if X[self.date_column_name].min() > self.split_dates.min():
                validation_error.append(
                    f"max split date {self.split_dates.min()} is larger "
                    f"than max date in the data {X[self.date_column_name].min()}"
                )
        except TypeError as e:
            validation_error.append(str(e))

        if not pd.Index(X[self.date_column_name]).is_monotonic:
            validation_error.append("X data is not temporally sorted")

        if not pd.Index(y.index).is_monotonic:
            validation_error.append("y data is not temporally sorted")

        return validation_error

    def get_parameters(self) -> dict:
        return {self.lbl_split_dates: self.split_dates, self.lbl_date_column_name: self.date_column_name}

    def _get_all_split_dates(self) -> pd.DatetimeIndex:
        return self.split_dates
