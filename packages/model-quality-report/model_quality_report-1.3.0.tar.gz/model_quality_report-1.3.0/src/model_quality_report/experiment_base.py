from abc import abstractmethod, ABC
from typing import Type

import pandas as pd

from model_quality_report.model_base import ModelBase
from model_quality_report.model_comparison_report import ExperimentKeyType
from model_quality_report.quality_report.base import QualityReportBase
from model_quality_report.splitters.base import SplitterBase


class ExperimentBase(ABC):
    def get_quality_report(self) -> QualityReportBase:
        return self._quality_report_class(model=self._get_model(), splitter=self._get_splitter())

    @abstractmethod
    def get_experiment_key(self) -> ExperimentKeyType:
        pass

    @abstractmethod
    def get_x_data(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_y_data(self) -> pd.Series:
        pass

    @property
    @abstractmethod
    def _quality_report_class(self) -> Type[QualityReportBase]:
        pass

    @abstractmethod
    def _get_model(self) -> ModelBase:
        pass

    @abstractmethod
    def _get_splitter(self) -> SplitterBase:
        pass
