from abc import ABC, abstractmethod
from typing import List, Tuple, Generator

import pandas as pd

Split = Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]
Splits = List[Split]
SplitGenerator = Generator[Split, None, None]


class SplitterBase(ABC):
    """
    Base metaclass for splitting data.
    """

    @abstractmethod
    def split(self, X: pd.DataFrame, y: pd.Series) -> SplitGenerator:
        """
        Given a data frame containing features and a series containing corresponding targets, a split into training
        and test data is performed, which are subsequently returned.
        :return: X_train, X_test, y_train, y_test
        """

    @abstractmethod
    def validate_parameters(self, X: pd.DataFrame, y: pd.Series) -> List[str]:
        """
        A splitting strategy can depend on various parameters, like e.g. the size of the test set or a date  after which
        all data are declared as test data. This functions validates that data and parameters fit to each other.
        :return: error
        """

    @abstractmethod
    def get_parameters(self) -> dict:
        """
        Returns parameters of Splitter as dict
        :return: dict of parameters
        """
