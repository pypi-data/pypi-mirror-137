from typing import List

import pandas as pd
from pandas.core.dtypes.common import is_datetime64_ns_dtype

from model_quality_report.splitters.base import SplitterBase, Split, SplitGenerator


class ByFrequency(SplitterBase):
    """
    Produces a list of splits of temporal data such that all observations
    after the specified date is used as test data until the input data is exhausted.

    This class can be of use in Time Series analysis, where one wants to produce predictions for several steps ahead
    starting at different dates, in order to assess predictive power of a model by averaging errors across these dates
    for each specific horizon.

    The X data used by this splitter has to have a `datetime64[ns]` column, and it has to be sorted along this column.
    The y data used by this splitter has to have `pd.DatetimeIndex` as its index and it has to be sorted along this index.

    Example
    -------
    import pandas as pd
    from model_quality_report.splitters.temporal.cross_validation.by_frequency import ByFrequency

    lbl_date = 'date'
    dates = pd.Index(pd.date_range('2019-01-01', periods=6), name=lbl_date)
    X = pd.DataFrame({'a': [1, 2, 4, 5, 7, 20],
                      'b': [3, 5, 7, 10, 15, 30],
                      lbl_date: dates})
    y = pd.Series([3, 6, 8, 10, 12, 30], index=dates)
    splitter = ByFrequency(start_split_date=dates[2], frequency="D", date_column_name=lbl_date)
    splitter.split(X, y)

    """

    lbl_date_column_name = "date_column_name"
    lbl_start_split_date = "start_split_date"
    lbl_end_split_date = "end_split_date"
    lbl_frequency = "frequency"

    def __init__(
        self, start_split_date: pd.Timestamp, date_column_name: str, frequency: str, end_split_date: pd.Timestamp = None
    ) -> None:
        self.start_split_date = start_split_date
        self.end_split_date = end_split_date
        self.date_column_name = date_column_name
        self.frequency = frequency

    def split(self, X: pd.DataFrame, y: pd.Series) -> SplitGenerator:
        """
        Given df with features X, target series y and test config, data are split into test and training data
        taking data from last time_delta long period as test data and the rest as training data.

        :param X:
        :param y:
        :return: list of (X_train, X_test, y_train, y_test)
        """
        for split_date in self._get_all_split_dates(X=X):
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
            if X[self.date_column_name].max() < self.start_split_date:
                validation_error.append(
                    f"start split date {self.start_split_date} is larger "
                    f"than max date {X[self.date_column_name].max()}"
                )
            if X[self.date_column_name].min() > self.start_split_date:
                validation_error.append(
                    f"start split date {self.start_split_date} is smaller "
                    f"than min date {X[self.date_column_name].min()}"
                )
            if self.end_split_date is not None:
                if self.start_split_date >= self.end_split_date:
                    validation_error.append(
                        f"start split date {self.start_split_date} is not smaller "
                        f"than end split date {self.end_split_date}"
                    )
                if X[self.date_column_name].max() < self.end_split_date:
                    validation_error.append(
                        f"end split date {self.end_split_date} is larger "
                        f"than max date {X[self.date_column_name].max()}"
                    )
                if X[self.date_column_name].min() > self.end_split_date:
                    validation_error.append(
                        f"end split date {self.end_split_date} is smaller "
                        f"than min date {X[self.date_column_name].min()}"
                    )
        except TypeError as e:
            validation_error.append(str(e))

        try:
            pd.date_range("2020-01-01", periods=1, freq=self.frequency)
        except ValueError as e:
            validation_error.append(str(e))

        if not pd.Index(X[self.date_column_name]).is_monotonic:
            validation_error.append("X data is not temporally sorted")

        if not pd.Index(y.index).is_monotonic:
            validation_error.append("y data is not temporally sorted")

        return validation_error

    def get_parameters(self) -> dict:
        return {
            self.lbl_start_split_date: self.start_split_date,
            self.lbl_end_split_date: self.end_split_date,
            self.lbl_date_column_name: self.date_column_name,
            self.lbl_frequency: self.frequency,
        }

    def _get_all_split_dates(self, X: pd.DataFrame) -> pd.DatetimeIndex:
        return pd.date_range(
            start=self.start_split_date,
            end=X[self.date_column_name].max() if self.end_split_date is None else self.end_split_date,
            freq=self.frequency,
        )
