from typing import List, Type

import pandas as pd

from model_quality_report.experiment_base import ExperimentBase
from model_quality_report.model_base import ModelBase
from model_quality_report.model_comparison_report import ExperimentKeyType
from model_quality_report.quality_report.base import QualityReportBase
from model_quality_report.quality_report.crossvalidation_timeseries import CrossValidationTimeSeriesQualityReport
from model_quality_report.splitters.base import SplitterBase
from model_quality_report.splitters.temporal.cross_validation.by_horizon import ByHorizon
from tests.models_for_tests import LinearModelWrapper, ClassifierModelWrapper


class LinearModelExperiment(ExperimentBase):
    def __init__(self, x_data: pd.DataFrame, y_data: pd.Series, exog_cols: List[str], experiment_key: str) -> None:
        self._x_data = x_data
        self._y_data = y_data
        self._exog_cols = exog_cols
        self._experiment_key = experiment_key

    @property
    def _quality_report_class(self) -> Type[QualityReportBase]:
        return CrossValidationTimeSeriesQualityReport

    def get_experiment_key(self) -> ExperimentKeyType:
        return {self._experiment_key: str(self._exog_cols)}

    def get_x_data(self) -> pd.DataFrame:
        return self._x_data

    def get_y_data(self) -> pd.Series:
        return self._y_data

    def _get_model(self) -> ModelBase:
        return LinearModelWrapper(exog_cols=self._exog_cols)

    def _get_splitter(self) -> SplitterBase:
        return ByHorizon(start_split_date=self._x_data.index[2], maximum_horizon=3)


class ClassifierModelExperiment(LinearModelExperiment):
    def _get_model(self) -> ModelBase:
        return ClassifierModelWrapper(exog_cols=self._exog_cols)
