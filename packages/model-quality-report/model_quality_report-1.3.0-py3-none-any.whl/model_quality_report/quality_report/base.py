import copy
import logging
import warnings
from abc import ABC, abstractmethod
from typing import List, Union, Dict

import pandas as pd

from model_quality_report.model_base import ModelBase
from model_quality_report.quality_metrics import all_quality_metrics
from model_quality_report.quality_report.quality_report_error import QualityReportError
from model_quality_report.splitters.base import SplitterBase, SplitGenerator

PandasObj = Union[pd.Series, pd.DataFrame]
QualityReportType = Dict[str, PandasObj]


class QualityReportBase(ABC):
    """
    Base metaclass for _model quality reports.

    """

    lbl_metrics = "metrics"
    lbl_data = "data"
    lbl_true_values = "true"
    lbl_predicted_values = "predicted"
    lbl_metric_value = "value"

    def __init__(self, model: ModelBase, splitter: SplitterBase) -> None:
        self._model = copy.deepcopy(model)
        self._splitter = splitter
        self._errors = QualityReportError()
        self._logger = logging.getLogger(self.__class__.__name__)

    def create_quality_report(self, X: pd.DataFrame, y: pd.Series) -> QualityReportType:
        """
        Given a _model and a data set a report on _model performance is created.

        :return: dict containing the quality report
        """
        y_test_all = list()
        predictions_all = list()

        if not self._errors.is_empty():
            return dict()

        for X_train, X_test, y_train, y_test in self._split_data_for_quality_assessment(X=X, y=y):

            try:
                self._fit(X_train, y_train)
                predictions = self._predict(X_test)
            except (RuntimeError, ValueError) as e:
                self._logger.error(str(e))
                self._errors.add(str(e))
                return dict()
            else:
                y_test_all.append(y_test)
                predictions_all.append(predictions)

        return self._create_dict_from_test_values_and_predictions(y_trues=y_test_all, y_preds=predictions_all)

    def _split_data_for_quality_assessment(self, X: pd.DataFrame, y: pd.Series) -> SplitGenerator:
        """
        Given features X and target y are split into training and test data.

        :return:
        """
        splits = list()
        validation_error = self._splitter.validate_parameters(X=X, y=y)
        if len(validation_error) == 0:
            splits = self._splitter.split(X=X, y=y)
        else:
            msg = "Split failed: {}".format(validation_error)
            self._logger.error(msg)
            self._errors.add(msg)
        return splits

    def _fit(self, X_train: pd.DataFrame, y_train: pd.Series) -> None:
        """
        Fits _model if it has a fit attribute

        :return:
        """
        try:
            self._model.fit(X_train, y_train)
        except (RuntimeError, AttributeError, ValueError) as e:
            self._logger.error(str(e))
            self._errors.add(str(e))

    def _predict(self, X_test: pd.DataFrame) -> pd.Series:
        """
        Predicts with _model if it has a predict attribute and returns predictions

        :return:
        """
        predictions = pd.Series(dtype=float)
        try:
            predictions = self._model.predict(X_test)
        except (RuntimeError, AttributeError, ValueError) as e:
            self._logger.error(str(e))
            self._errors.add(str(e))
        if not isinstance(predictions, pd.Series):
            predictions = pd.Series(predictions, index=X_test.index)
        return predictions

    @staticmethod
    def _true_and_predicted_values_as_pandas(y_true: PandasObj, y_pred: PandasObj) -> PandasObj:
        return pd.merge(y_true, y_pred, left_index=True, right_index=True)

    def _create_dict_from_test_values_and_predictions(
        self, y_trues: List[pd.Series], y_preds: List[pd.Series]
    ) -> QualityReportType:
        """Create report from test and predicted values of y.

        :param y_trues: list of true values of y
        :param y_preds: list of predicted values of y
        :return: quality report in dictionary format
        """
        y_trues = self._convert_list_of_data_to_pandas(data=y_trues, name=self.lbl_true_values)
        y_preds = self._convert_list_of_data_to_pandas(data=y_preds, name=self.lbl_predicted_values)

        if y_trues.index.names != y_preds.index.names:
            msg = (
                f"Test and predictions index names are different. "
                f"Test index names: {y_trues.index.names}. "
                f"Prediction index names: {y_preds.index.names}."
            )
            self._logger.error(msg)
            self._errors.add(msg)
            return dict()

        return {
            self.lbl_metrics: self._calculate_quality_metrics_as_pandas(y_true=y_trues, y_pred=y_preds),
            self.lbl_data: self._true_and_predicted_values_as_pandas(y_true=y_trues, y_pred=y_preds),
        }

    @staticmethod
    def _calculate_quality_metrics(y_true: pd.Series, y_pred: pd.Series) -> Dict[str, float]:
        """
        Given y_pred and y_true, various metrics are derived and returned as dict.

        :return: dict containing the quality metrics
        """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return {name: metric(y_true=y_true, y_pred=y_pred) for name, metric in all_quality_metrics.items()}

    @abstractmethod
    def _calculate_quality_metrics_as_pandas(self, y_true: PandasObj, y_pred: PandasObj) -> PandasObj:
        """
        Given y_pred and y_true, various metrics are derived and returned as pandas object.

        :return: Series or DataFrame containing the quality metrics
        """

    @abstractmethod
    def _convert_list_of_data_to_pandas(self, data: List[pd.Series], name: str = None) -> PandasObj:
        """Convert list of data to pandas object.

        This method is specific to quality report format.
        If a prediction is a scalar, then we return a Series of predictions for each split.
        If a prediction is array-like, e.g. time horizon along its dimension,
        then we return a DataFrame with rows for each split and columns for each horizon.

        :return: either Series or DataFrame depending on the report specifics
        """

    @classmethod
    def get_metrics(cls, report: dict) -> pd.DataFrame:
        """Convert quality report (only metrics part) from dictionary format into DataFrame.

        :return: DataFrame containing the quality report

        Example input
        -------------
        {'metrics':
        {'explained_variance_score': 0.9148351648351651,
        'mape': 0.4388888888888885,
        mean_absolute_error': 6.66666666666666,
        'mean_squared_error': 51.33333333333321,
        'median_absolute_error': 7.999999999999986,
        'r2_score': 0.365384615384617},
        'data':
        {'true': {4: 12, 3: 10, 5: 30},
        'predicted': {4: 20.999999999999993, 3: 12.999999999999998, 5: 37.999999999999986}}}

        Example output
        --------------
                            metrics      value
        0  explained_variance_score   0.914835
        1                      mape   0.438889
        2       mean_absolute_error   6.666667
        3        mean_squared_error  51.333333
        4     median_absolute_error   8.000000
        5                  r2_score   0.365385

        """
        return report.get(cls.lbl_metrics)

    @classmethod
    def get_true_and_predicted_data(cls, report: dict) -> pd.DataFrame:
        return report.get(cls.lbl_data)

    def get_errors(self) -> QualityReportError:
        return self._errors
