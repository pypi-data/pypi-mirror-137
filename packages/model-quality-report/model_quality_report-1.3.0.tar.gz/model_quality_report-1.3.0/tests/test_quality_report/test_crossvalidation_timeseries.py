import unittest

import numpy as np
import pandas as pd
from parameterized import parameterized_class

from model_quality_report.quality_metrics import all_quality_metrics
from model_quality_report.quality_report.crossvalidation_timeseries import CrossValidationTimeSeriesQualityReport
from model_quality_report.splitters.random import RandomDataSplitter
from model_quality_report.splitters.temporal.cross_validation.by_frequency import ByFrequency
from model_quality_report.splitters.temporal.cross_validation.by_horizon import ByHorizon
from model_quality_report.splitters.temporal.cross_validation.fixed_dates import FixedDates
from tests.models_for_tests import LinearModelWrapper, LinearModelWrapperWithIndexName

by_horizon = ByHorizon(start_split_date=pd.Timestamp("2019-01-03"), maximum_horizon=2)
by_frequency = ByFrequency(start_split_date=pd.Timestamp("2019-01-03"), frequency="D", date_column_name="date")
fixed_dates = FixedDates(split_dates=pd.date_range(start="2019-01-03", periods=3), date_column_name="date")


@parameterized_class(
    [
        {"splitter": by_horizon, "len_metrics": 2},
        {"splitter": by_frequency, "len_metrics": 5},
        {"splitter": fixed_dates, "len_metrics": 2},
    ]
)
class Test2DQualityReport(unittest.TestCase):
    def setUp(self):
        self.lbl_date = "date"
        dates = pd.date_range("2019-01-01", periods=7)
        self.index = pd.DatetimeIndex(dates, name=self.lbl_date)
        self.X = pd.DataFrame(
            {"a": [1, 2, 4, 5, 7, 20, 6], "b": [3, 5, 7, 10, 15, 30, 22], "date": dates},
            index=self.index,
        )
        self.y = pd.Series([3, 6, 8, 10, 12, 30, 23], index=self.index)
        self.model = LinearModelWrapper(exog_cols=["a", "b"])
        self.maximum_horizon = 2
        self.frequency = "D"

    def test_calculate_metrics(self):
        y_true = pd.Series([3, -0.5, 2, 7])
        y_pred = pd.Series([2.5, 0.0, 2, 8])

        metrics = CrossValidationTimeSeriesQualityReport._calculate_quality_metrics(y_true, y_pred)
        result_dict = {name: metric(y_true, y_pred) for name, metric in all_quality_metrics.items()}

        self.assertTrue(isinstance(metrics, dict))
        self.assertDictEqual(metrics, result_dict)

    def test_splitting_fails_and_returns_error(self):
        wrong_splitter = RandomDataSplitter(test_size=10)
        quality_report = CrossValidationTimeSeriesQualityReport(self.model, wrong_splitter)
        quality_report._split_data_for_quality_assessment(self.X, self.y)

        self.assertTrue("Split failed" in quality_report._errors.to_string())

    def test_fit_does_not_create_error_when_proper_model_is_provided(self):
        quality_report = CrossValidationTimeSeriesQualityReport(self.model, self.splitter)
        (X_train, X_test, y_train, y_test,) = list(
            quality_report._split_data_for_quality_assessment(self.X, self.y)
        )[0]
        quality_report._fit(X_train, y_train)

        self.assertTrue(quality_report._errors.is_empty())

    def test_quality_report_contains_error_if_fit_attribute_is_not_present(self):
        quality_report = CrossValidationTimeSeriesQualityReport("no_model_but_string", self.splitter)
        (X_train, X_test, y_train, y_test,) = list(
            quality_report._split_data_for_quality_assessment(self.X, self.y)
        )[0]
        quality_report._fit(X_train, y_train)

        self.assertFalse(quality_report._errors.is_empty())
        self.assertTrue("fit" in quality_report._errors.to_string())

    def test_predict_does_not_create_error_when_proper_model_is_provided(self):
        quality_report = CrossValidationTimeSeriesQualityReport(self.model, self.splitter)
        (X_train, X_test, y_train, y_test,) = list(
            quality_report._split_data_for_quality_assessment(self.X, self.y)
        )[0]
        quality_report._fit(X_train, y_train)
        prediction_result = quality_report._predict(X_test)

        self.assertTrue(quality_report._errors.is_empty())
        self.assertIsInstance(prediction_result, pd.Series)
        self.assertTrue(len(prediction_result), len(y_train))

    def test_error_when_test_predict_not_aligned(self):
        quality_report = CrossValidationTimeSeriesQualityReport(self.model, self.splitter)

        def _convert_list_of_data_to_pandas(data, name):
            df_list = [pd.DataFrame({name: df, quality_report.lbl_horizon: np.arange(df.shape[0])}) for df in data]
            return (
                pd.concat(df_list)
                .set_index(quality_report.lbl_horizon, append=True)
                .pipe(lambda x: x.sort_values(by=x.columns[0]))
            )

        quality_report._convert_list_of_data_to_pandas = _convert_list_of_data_to_pandas

        result = quality_report.create_quality_report(self.X, self.y)

        self.assertTrue(quality_report._errors.is_empty())
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(
            [CrossValidationTimeSeriesQualityReport.lbl_metrics, CrossValidationTimeSeriesQualityReport.lbl_data],
            list(result.keys()),
        )
        self.assertTrue(isinstance(result[CrossValidationTimeSeriesQualityReport.lbl_metrics], pd.DataFrame))
        self.assertTrue(isinstance(result.get(CrossValidationTimeSeriesQualityReport.lbl_data), pd.DataFrame))

    def test_quality_report_contains_error_if_fit_and_predict_attribute_are_not_present(self):
        for model in [None, "no_model_but_string"]:
            quality_report = CrossValidationTimeSeriesQualityReport(model, self.splitter)
            (X_train, X_test, y_train, y_test,) = list(
                quality_report._split_data_for_quality_assessment(self.X, self.y)
            )[0]
            quality_report._fit(X_train, y_train)
            prediction_result = quality_report._predict(X_test)

            self.assertFalse(quality_report._errors.is_empty())
            self.assertTrue("fit" in quality_report._errors.to_string())
            self.assertTrue("predict" in quality_report._errors.to_string())
            self.assertIsInstance(prediction_result, pd.Series)

    def test_quality_report_is_properly_returned(self):
        index_name = "another"
        self.model = LinearModelWrapperWithIndexName(exog_cols=["a", "b"], index_name=index_name)
        quality_report = CrossValidationTimeSeriesQualityReport(self.model, self.splitter)

        result = quality_report.create_quality_report(self.X, self.y)

        self.assertEqual(result, dict())
        self.assertFalse(quality_report.get_errors().is_empty())
        self.assertIn(index_name, quality_report.get_errors().to_string())

    def test_quality_report_is_empty_if_index_names_are_different(self):
        quality_report = CrossValidationTimeSeriesQualityReport(self.model, self.splitter)

        result = quality_report.create_quality_report(self.X, self.y)

        self.assertTrue(isinstance(result, dict))
        self.assertEqual(
            [CrossValidationTimeSeriesQualityReport.lbl_metrics, CrossValidationTimeSeriesQualityReport.lbl_data],
            list(result.keys()),
        )
        self.assertTrue(isinstance(result[CrossValidationTimeSeriesQualityReport.lbl_metrics], pd.DataFrame))
        self.assertTrue(isinstance(result.get(CrossValidationTimeSeriesQualityReport.lbl_data), pd.DataFrame))

    def test_create_quality_report_data_format(self):
        quality_report = CrossValidationTimeSeriesQualityReport(self.model, self.splitter)
        result = quality_report.create_quality_report(X=self.X, y=self.y)

        metrics = quality_report.get_metrics(report=result)
        self.assertIsInstance(metrics, pd.DataFrame)
        self.assertEqual(
            set(metrics.columns),
            {quality_report.lbl_metrics, quality_report.lbl_metric_value, quality_report.lbl_horizon},
        )
        pd.testing.assert_frame_equal(metrics, result.get(quality_report.lbl_metrics))

        data = quality_report.get_true_and_predicted_data(report=result)
        self.assertIsInstance(data, pd.DataFrame)
        self.assertEqual(
            set(data.columns),
            {quality_report.lbl_true_values, quality_report.lbl_predicted_values},
        )
        self.assertEqual({quality_report.lbl_horizon, self.lbl_date}, set(data.index.names))
        pd.testing.assert_frame_equal(data, result.get(quality_report.lbl_data))
