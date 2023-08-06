from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd


class ModelBase(ABC):
    """
    Base metaclass for model provided to quality report library. It is basically used to provide type hints.

    """

    @abstractmethod
    def fit(self, X_train: pd.DataFrame, y_train: pd.Series) -> ModelBase:
        """
        Each model passed to quality report must have a fit function
        """

    @abstractmethod
    def predict(self, X_test: pd.DataFrame) -> pd.Series:
        """
        Each model passed to quality report must have a predict function
        """
