import unittest

import pandas as pd
from parameterized import parameterized_class
from sklearn import linear_model

from model_quality_report.model_comparison_report import ModelComparisonReport
from model_quality_report.quality_report.base import QualityReportBase
from model_quality_report.quality_report.crossvalidation_timeseries import (
    CrossValidationTimeSeriesQualityReport,
)
from model_quality_report.quality_report.regression import (
    RegressionQualityReport,
)
from model_quality_report.splitters.random import RandomDataSplitter
from model_quality_report.splitters.temporal.cross_validation.by_horizon import (
    ByHorizon,
)
from tests.models_for_tests import LinearModelWrapper


@parameterized_class(("n_jobs",), [(None,), (-1,)])
class TestCrossValidationModelComparisonReport(unittest.TestCase):
    def setUp(self):
        self.lbl_date = "date"
        self.lbl_model = "model"
        self.lbl_yname = "y name"
        self.lbl_model_name1 = "Model 1"
        self.lbl_model_name2 = "Model 2"
        dates = pd.date_range("2019-01-01", periods=8)
        self.index = pd.DatetimeIndex(dates, name=self.lbl_date)
        self.X = pd.DataFrame(
            {
                "a": [1, 2, 4, 5, 7, 20, 6, 11],
                "b": [3, 5, 7, 10, 15, 30, 22, 48],
                "c": [8, 1, 0, 17, 11, 20, 2, 4],
            },
            index=self.index,
        )
        y1 = pd.Series([3, 6, 8, 10, 12, 30, 23, 5], name="y1", index=self.index)
        y2 = pd.Series([3, 6, 8, 10, 12, 30, 23, 5], name="y2", index=self.index)
        model1 = LinearModelWrapper(exog_cols=["a", "b"])
        model2 = LinearModelWrapper(exog_cols=["b", "c"])
        self.maximum_horizon = 3
        self.splitter = ByHorizon(start_split_date=dates[2], maximum_horizon=self.maximum_horizon)
        self.quality_reports = [
            CrossValidationTimeSeriesQualityReport(model=model, splitter=self.splitter)
            for model in [model1, model2, model2]
        ]
        self.X_data_list = [self.X for _ in range(3)]
        self.y_data_list = [y1, y2, y1]
        self.experiment_keys = [
            {self.lbl_model: self.lbl_model_name1, self.lbl_yname: y1.name},
            {self.lbl_model: self.lbl_model_name2, self.lbl_yname: y2.name},
            {self.lbl_model: self.lbl_model_name2, self.lbl_yname: y1.name},
        ]

    def test_basic_model_comparison_results(self):
        model_comparison = ModelComparisonReport(
            quality_reports=self.quality_reports,
            X_data_list=self.X_data_list,
            y_data_list=self.y_data_list,
            experiment_keys=self.experiment_keys,
            n_jobs=self.n_jobs,
        )
        reports = model_comparison.create_reports()

        self.assertIsInstance(reports, list)
        for report in reports:
            self.assertIsInstance(report, dict)
            self.assertEqual(len(report), 3)

        for report, experiment_key in zip(reports, self.experiment_keys):
            self.assertEqual(report.get(model_comparison.lbl_experiment_key), experiment_key)
            self.assertIsInstance(report.get(model_comparison.lbl_report), dict)
            self.assertIsInstance(report.get(model_comparison.lbl_errors), str)

    def test_report_conversion(self):
        model_comparison = ModelComparisonReport(
            quality_reports=self.quality_reports,
            X_data_list=self.X_data_list,
            y_data_list=self.y_data_list,
            experiment_keys=self.experiment_keys,
            n_jobs=self.n_jobs,
        )
        reports = model_comparison.create_reports()
        result_df = model_comparison.get_metrics(reports=reports)

        self.assertIsInstance(result_df, pd.DataFrame)
        self.assertIn(self.lbl_model, result_df.columns)
        self.assertIn(self.lbl_yname, result_df.columns)
        self.assertIn(model_comparison.lbl_metrics, result_df.columns)
        self.assertIn(model_comparison.lbl_metric_value, result_df.columns)

        result_df = model_comparison.get_true_and_predicted_data(reports=reports)

        self.assertIsInstance(result_df, pd.DataFrame)
        self.assertIn(QualityReportBase.lbl_true_values, result_df.columns)
        self.assertIn(QualityReportBase.lbl_predicted_values, result_df.columns)
        self.assertIn(self.lbl_model, result_df.columns)
        self.assertIn(self.lbl_yname, result_df.columns)
        self.assertIn(CrossValidationTimeSeriesQualityReport.lbl_horizon, result_df.index.names)
        self.assertIn(self.lbl_date, result_df.index.names)


@parameterized_class(("n_jobs",), [(None,), (-1,)])
class TestRegressionModelComparisonReport(unittest.TestCase):
    def setUp(self):
        self.X = pd.DataFrame({"a": [1, 2, 4, 5, 7, 20], "b": [3, 5, 7, 10, 15, 30]})
        self.y = pd.Series([3, 6, 8, 10, 12, 30], name="y")
        self.model = linear_model.LinearRegression()
        self.test_size = 0.5
        self.splitter = RandomDataSplitter(test_size=self.test_size)
        self.lbl_model = "model"
        self.lbl_exog = "exogenous"
        self.lbl_model_name = "Model"
        self.exog_cols1 = ["a", "b"]
        self.exog_cols2 = ["a"]
        self.exog_cols3 = ["b"]

        self.quality_reports = [RegressionQualityReport(model=self.model, splitter=self.splitter) for _ in range(3)]
        self.X_data_list = [self.X[cols] for cols in [self.exog_cols1, self.exog_cols2, self.exog_cols3]]
        self.y_data_list = [self.y for _ in range(3)]
        self.experiment_keys = [
            {
                self.lbl_model: self.lbl_model_name,
                self.lbl_exog: ", ".join(cols),
            }
            for cols in [self.exog_cols1, self.exog_cols2, self.exog_cols3]
        ]

    def test_basic_model_comparison_results(self):
        model_comparison = ModelComparisonReport(
            quality_reports=self.quality_reports,
            X_data_list=self.X_data_list,
            y_data_list=self.y_data_list,
            experiment_keys=self.experiment_keys,
            n_jobs=self.n_jobs,
        )
        if self.n_jobs is None:
            with self.assertLogs(level="INFO") as caplog:
                reports = model_comparison.create_reports()
        else:
            reports = model_comparison.create_reports()

        self.assertIsInstance(reports, list)
        for report in reports:
            self.assertIsInstance(report, dict)
            self.assertEqual(len(report), 3)

        for report, experiment_key, quality_report_instance, y_data, x_data in zip(
            reports, self.experiment_keys, self.quality_reports, self.y_data_list, self.X_data_list
        ):
            self.assertEqual(report[model_comparison.lbl_experiment_key], experiment_key)
            self.assertIsInstance(report[model_comparison.lbl_report], dict)
            self.assertIsInstance(report[model_comparison.lbl_errors], str)
            if self.n_jobs is None:
                self.assertIn(str(experiment_key), "".join(caplog.output))
                self.assertIn(str(quality_report_instance.__class__.__name__), "".join(caplog.output))
                self.assertIn(y_data.name, "".join(caplog.output))
                self.assertIn(str(y_data.shape), "".join(caplog.output))
                self.assertIn(str(x_data.columns.values), "".join(caplog.output))
                self.assertIn(str(x_data.shape), "".join(caplog.output))

    def test_report_conversion(self):
        model_comparison = ModelComparisonReport(
            quality_reports=self.quality_reports,
            X_data_list=self.X_data_list,
            y_data_list=self.y_data_list,
            experiment_keys=self.experiment_keys,
            n_jobs=self.n_jobs,
        )
        reports = model_comparison.create_reports()
        result_df = model_comparison.get_metrics(reports=reports)

        self.assertIsInstance(result_df, pd.DataFrame)
        self.assertIn(self.lbl_model, result_df.columns)
        self.assertIn(self.lbl_exog, result_df.columns)
        self.assertIn(model_comparison.lbl_metrics, result_df.columns)
        self.assertIn(model_comparison.lbl_metric_value, result_df.columns)

        result_df = model_comparison.get_true_and_predicted_data(reports=reports)

        self.assertIsInstance(result_df, pd.DataFrame)
        self.assertIn(QualityReportBase.lbl_true_values, result_df.columns)
        self.assertIn(QualityReportBase.lbl_predicted_values, result_df.columns)
        self.assertIn(self.lbl_model, result_df.columns)
        self.assertIn(self.lbl_exog, result_df.columns)
