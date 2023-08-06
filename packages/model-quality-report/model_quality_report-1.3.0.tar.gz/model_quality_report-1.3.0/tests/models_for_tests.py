from __future__ import annotations

from typing import List

import pandas as pd
from numpy import ndarray
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVC

from model_quality_report.model_base import ModelBase


class LinearModelWrapper(ModelBase):
    def __init__(self, exog_cols: List[str]) -> None:
        self._exog_cols = exog_cols
        self.model = LinearRegression()

    def fit(self, X_train: pd.DataFrame, y_train: pd.Series) -> LinearModelWrapper:
        self.model.fit(X_train[self._exog_cols], y_train)
        return self

    def predict(self, X_test: pd.DataFrame) -> ndarray:
        return self.model.predict(X_test[self._exog_cols])


class LinearModelWrapperWithIndexName(LinearModelWrapper):
    def __init__(self, index_name: str, **kwargs):
        super().__init__(**kwargs)
        self._index_name = index_name

    def predict(self, X_test: pd.DataFrame) -> pd.Series:
        return pd.Series(
            self.model.predict(X_test[self._exog_cols]),
            index=pd.Index(X_test.index, name=self._index_name),
        )


class ClassifierModelWrapper(ModelBase):
    def __init__(self, exog_cols: List[str]) -> None:
        self._exog_cols = exog_cols
        self.model = SVC()

    def fit(self, X_train: pd.DataFrame, y_train: pd.Series) -> ClassifierModelWrapper:
        self.model.fit(X_train[self._exog_cols], y_train)
        return self

    def predict(self, X_test: pd.DataFrame) -> ndarray:
        return self.model.predict(X_test[self._exog_cols])
