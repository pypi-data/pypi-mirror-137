import logging
import time
from typing import List, TypedDict, Optional

import pandas as pd
from joblib import Parallel, delayed

from model_quality_report.quality_report.base import QualityReportBase, QualityReportType

ExperimentKeyType = dict


class ModelComparisonReportType(TypedDict):
    experiment_key: ExperimentKeyType
    report: QualityReportType
    errors: str


class ModelComparisonReport:
    """Model comparison report.

    It takes four lists of equal size: `QualityReportBase` instances, `X_data_list`, `y_data_list`,
    and flat dictionaries `experiment_keys`. The class now has only two public methods:
      - `create_reports` that simply returns the list quality reports for each experiment, and
      - `get_metrics` that extracts a single metrics DataFrame from multiple quality reports obtained above.
       The resulting DataFrame has experiment keys in corresponding columns.
    """

    lbl_metrics = QualityReportBase.lbl_metrics
    lbl_metric_value = QualityReportBase.lbl_metric_value

    lbl_experiment_key = "experiment_key"
    lbl_report = "report"
    lbl_errors = "errors"

    def __init__(
        self,
        quality_reports: List[QualityReportBase],
        X_data_list: List[pd.DataFrame],
        y_data_list: List[pd.Series],
        experiment_keys: List[ExperimentKeyType],
        n_jobs: Optional[int] = None,
    ) -> None:
        """

        :param quality_reports: list of `QualityReportBase` instances
        that would produce a quality report for each experiment.
        :param X_data_list: list of X data
        :param y_data_list: list of y data
        :param experiment_keys: list of flat dictionaries that provide a description for each experiment
        :param n_jobs: the maximum number of concurrently running jobs (see `joblib.Parallel`)
        """
        self._quality_reports = quality_reports
        self._X_data_list = X_data_list
        self._y_data_list = y_data_list
        self._experiment_keys = experiment_keys
        self._n_jobs = n_jobs
        self._logger = logging.getLogger(self.__class__.__name__)

    def create_reports(self) -> List[ModelComparisonReportType]:
        """
        Given a list of experiments compute quality reports for each and combine them in one dictionary.

        :return: dict containing the quality report
        """
        experiments = zip(self._experiment_keys, self._quality_reports, self._X_data_list, self._y_data_list)
        with Parallel(n_jobs=self._n_jobs, verbose=10, backend="loky") as parallel:
            results = parallel(
                delayed(create_reports_kernel)(experiment_key=experiment_key, quality_report=quality_report, X=X, y=y)
                for experiment_key, quality_report, X, y in experiments
            )
        return results

    def get_metrics(self, reports: List[ModelComparisonReportType]) -> pd.DataFrame:
        """Convert quality reports (only metrics part) into a single DataFrame.

        :return: DataFrame containing metric values for each experiment

        Example output
        --------------
                            metrics     value  model  exogenous
        0  explained_variance_score  0.949841  Model1      a, b
        1                      mape  0.177778  Model1      a, b
        2       mean_absolute_error  1.000000  Model1      a, b
        3        mean_squared_error  1.240000  Model1      a, b
        4     median_absolute_error  1.000000  Model1      a, b
        5                  r2_score  0.911429  Model1      a, b
        0  explained_variance_score  0.992172  Model2         a
        1                      mape  0.187302  Model2         a
        2       mean_absolute_error  0.952381  Model2         a
        3        mean_squared_error  1.142857  Model2         a
        4     median_absolute_error  1.142857  Model2         a
        5                  r2_score  0.992172  Model2         a
        0  explained_variance_score  0.973807  Model3         b
        1                      mape  0.158055  Model3         b
        2       mean_absolute_error  0.861451  Model3         b
        3        mean_squared_error  0.957465  Model3         b
        4     median_absolute_error  0.577017  Model3         b
        5                  r2_score  0.883552  Model3         b

        """
        results = list()
        for quality_report_instance, quality_report in zip(self._quality_reports, reports):
            report_df = quality_report_instance.get_metrics(report=quality_report[self.lbl_report]).assign(
                **quality_report[self.lbl_experiment_key]
            )
            results.append(report_df)
        return pd.concat(results)

    def get_true_and_predicted_data(self, reports: List[ModelComparisonReportType]) -> pd.DataFrame:
        """Convert quality reports (true and predicted values) into a single DataFrame.

        :param reports:
        :return: DataFrame containing metric values for each experiment

        Example output
        --------------
                            true  predicted    model y name
        date       horizon
        2019-01-03 0           8   9.600000  Model 1     y1
        2019-01-04 1          10  13.800000  Model 1     y1
        2019-01-05 2          12  21.000000  Model 1     y1
        2019-01-03 0           8   6.622642  Model 2     y2
        2019-01-04 1          10   0.226415  Model 2     y2
        2019-01-05 2          12   3.169811  Model 2     y2
        2019-01-04 0          10   7.916667  Model 2     y2

        """
        results = list()
        for quality_report_instance, quality_report in zip(self._quality_reports, reports):
            report_df = quality_report_instance.get_true_and_predicted_data(
                report=quality_report[self.lbl_report]
            ).assign(**quality_report[self.lbl_experiment_key])
            results.append(report_df)
        return pd.concat(results)


def create_reports_kernel(
    experiment_key: ExperimentKeyType,
    quality_report: QualityReportBase,
    X: pd.DataFrame,
    y: pd.Series,
) -> ModelComparisonReportType:
    logger = logging.getLogger(__name__)
    msg = (
        f"experiment key: {experiment_key}, "
        f"quality report: {quality_report.__class__.__name__}, "
        f"y data shape: {y.shape}, and name: {y.name}, "
        f"X data shape; {X.shape}, and columns: {X.columns.values}."
    )
    logger.info(f"Start quality report for {msg}")
    start_time = time.perf_counter()
    report = quality_report.create_quality_report(X=X, y=y)
    logger.info(f"Finish quality report for {msg}")
    logger.info(f"Total time: {time.perf_counter() - start_time} seconds.")
    return ModelComparisonReportType(
        experiment_key=experiment_key, report=report, errors=quality_report.get_errors().to_string()
    )
