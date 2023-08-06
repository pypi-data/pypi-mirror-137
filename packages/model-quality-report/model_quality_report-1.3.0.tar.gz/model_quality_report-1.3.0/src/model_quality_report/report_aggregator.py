from typing import List, Optional, Union

import pandas as pd
from pandera.typing import DataFrame

from model_quality_report.experiment_base import ExperimentBase
from model_quality_report.model_comparison_report import (
    ModelComparisonReport,
    ModelComparisonReportType,
    ExperimentKeyType,
)
from model_quality_report.quality_report.base import QualityReportBase
from model_quality_report.schemas import (
    ModelQualityMetricsSchema,
    TrueAndPredictedFloatSchema,
    TrueAndPredictedBoolSchema,
)


class ReportAggregator:
    def __init__(self, experiments: List[ExperimentBase], n_jobs: Optional[int] = None) -> None:
        self._model_comparison = self._get_model_comparison(experiments=experiments, n_jobs=n_jobs)

    def run(self) -> List[ModelComparisonReportType]:
        return self._model_comparison.create_reports()

    def get_metrics(self, reports: List[ModelComparisonReportType]) -> DataFrame[ModelQualityMetricsSchema]:
        return self._model_comparison.get_metrics(reports=reports)

    def get_true_and_predicted_data(
        self, reports: List[ModelComparisonReportType]
    ) -> Union[DataFrame[TrueAndPredictedFloatSchema], DataFrame[TrueAndPredictedBoolSchema]]:
        return self._model_comparison.get_true_and_predicted_data(reports=reports).reset_index()

    def _get_model_comparison(
        self, experiments: List[ExperimentBase], n_jobs: Optional[int] = None
    ) -> ModelComparisonReport:
        return ModelComparisonReport(
            quality_reports=self._get_quality_reports(experiments=experiments),
            X_data_list=self._get_x_data_list(experiments=experiments),
            y_data_list=self._get_y_data_list(experiments=experiments),
            experiment_keys=self._get_experiment_keys(experiments=experiments),
            n_jobs=n_jobs,
        )

    @staticmethod
    def _get_quality_reports(experiments: List[ExperimentBase]) -> List[QualityReportBase]:
        return [experiment.get_quality_report() for experiment in experiments]

    @staticmethod
    def _get_x_data_list(experiments: List[ExperimentBase]) -> List[pd.DataFrame]:
        return [experiment.get_x_data() for experiment in experiments]

    @staticmethod
    def _get_y_data_list(experiments: List[ExperimentBase]) -> List[pd.Series]:
        return [experiment.get_y_data() for experiment in experiments]

    @staticmethod
    def _get_experiment_keys(experiments: List[ExperimentBase]) -> List[ExperimentKeyType]:
        return [experiment.get_experiment_key() for experiment in experiments]
