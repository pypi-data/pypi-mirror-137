import unittest
from typing import Optional

import pandas as pd
from pandera.errors import SchemaErrors
from parameterized import parameterized

from model_quality_report.report_aggregator import ReportAggregator
from model_quality_report.schemas import (
    ModelQualityMetricsSchema,
    TrueAndPredictedFloatSchema,
    TrueAndPredictedBoolSchema,
)
from tests.linear_model_experiment import LinearModelExperiment, ClassifierModelExperiment


class TestReportAggregator(unittest.TestCase):
    def setUp(self):
        dates = pd.date_range("2019-01-01", periods=8)
        index = pd.DatetimeIndex(dates, name="date")
        self.X = pd.DataFrame(
            {
                "a": [1.1, 2, 4, 5, 7, 20, 6, 11],
                "b": [3.3, 5, 7, 10, 15, 30, 22, 48],
                "c": [8.8, 1, 0, 17, 11, 20, 2, 4],
            },
            index=index,
        )
        self.y_data_float = pd.Series([3.4, 6, 8, 10, 12, 30, 23, 5], name="y1", index=index)
        self.y_data_bool = pd.Series([True, False, True, True, False, False, False, True], name="y2", index=index)

    @parameterized.expand([(None,), (-1,)])
    def test_report_aggregator_with_linear_model(self, n_jobs: Optional[int] = None):
        experiments = list()
        experiment_keys = ["key1", "key2"]
        for exog_cols, experiment_key in zip((["a", "b"], ["b", "c"]), experiment_keys):
            experiments.append(
                LinearModelExperiment(
                    x_data=self.X, y_data=self.y_data_float, exog_cols=exog_cols, experiment_key=experiment_key
                )
            )

        aggregator = ReportAggregator(experiments=experiments, n_jobs=n_jobs)
        reports = aggregator.run()
        metrics = aggregator.get_metrics(reports=reports)
        true_and_predicted = aggregator.get_true_and_predicted_data(reports=reports)

        ModelQualityMetricsSchema.validate(metrics, lazy=True)
        TrueAndPredictedFloatSchema.validate(true_and_predicted, lazy=True)
        with self.assertRaises(SchemaErrors):
            TrueAndPredictedBoolSchema.validate(true_and_predicted, lazy=True)
        for key in experiment_keys:
            self.assertIn(key, metrics.columns)
            self.assertIn(key, true_and_predicted.columns)

    @parameterized.expand([(None,), (-1,)])
    def test_report_aggregator_with_classifier_model(self, n_jobs: Optional[int] = None):
        experiments = list()
        experiment_keys = ["key1", "key2"]
        for exog_cols, experiment_key in zip((["a", "b"], ["b", "c"]), experiment_keys):
            experiments.append(
                ClassifierModelExperiment(
                    x_data=self.X, y_data=self.y_data_bool, exog_cols=exog_cols, experiment_key=experiment_key
                )
            )

        aggregator = ReportAggregator(experiments=experiments, n_jobs=n_jobs)
        reports = aggregator.run()
        metrics = aggregator.get_metrics(reports=reports)
        true_and_predicted = aggregator.get_true_and_predicted_data(reports=reports)

        ModelQualityMetricsSchema.validate(metrics, lazy=True)
        TrueAndPredictedBoolSchema.validate(true_and_predicted, lazy=True)
        with self.assertRaises(SchemaErrors):
            TrueAndPredictedFloatSchema.validate(true_and_predicted, lazy=True)
        for key in experiment_keys:
            self.assertIn(key, metrics.columns)
            self.assertIn(key, true_and_predicted.columns)
