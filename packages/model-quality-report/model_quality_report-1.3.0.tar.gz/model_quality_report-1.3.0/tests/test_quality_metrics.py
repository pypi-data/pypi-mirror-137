import unittest

import numpy as np
import pandas as pd
from sklearn.metrics import (
    explained_variance_score,
    mean_squared_error,
    mean_absolute_error,
    r2_score,
    accuracy_score,
    precision_score,
    recall_score,
)

from model_quality_report.quality_metrics import regression_quality_metrics, classification_quality_metrics


class TestQualityMetrics(unittest.TestCase):
    def test_quality_metrics(self):
        y_true = pd.Series([3, -0.5, 2, 7])
        y_pred = pd.Series([2.5, 0.0, 2, 8])
        rqm = regression_quality_metrics

        self.assertEqual(rqm.get("r2_score")(y_true, y_pred), r2_score(y_true, y_pred))
        self.assertEqual(
            rqm.get("explained_variance_score")(y_true, y_pred),
            explained_variance_score(y_true, y_pred),
        )
        self.assertEqual(rqm.get("mean_squared_error")(y_true, y_pred), mean_squared_error(y_true, y_pred))
        self.assertEqual(rqm.get("mean_absolute_error")(y_true, y_pred), mean_absolute_error(y_true, y_pred))
        self.assertEqual(rqm.get("median_absolute_error")(y_true, y_pred), np.median(np.abs(y_pred - y_true)))
        self.assertEqual(rqm.get("mean_error")(y_true, y_pred), np.mean(y_true - y_pred))
        self.assertEqual(rqm.get("median_error")(y_true, y_pred), np.median(y_true - y_pred))
        self.assertEqual(rqm.get("mean_percentage_error")(y_true, y_pred), np.mean((y_true - y_pred) / y_true))
        self.assertEqual(
            rqm.get("median_percentage_error")(y_true, y_pred),
            np.median((y_true - y_pred) / y_true),
        )
        self.assertEqual(
            rqm.get("mean_absolute_percentage_error")(y_true, y_pred),
            np.mean(np.abs((y_true - y_pred) / y_true)),
        )
        self.assertEqual(
            rqm.get("median_absolute_percentage_error")(y_true, y_pred),
            np.median(np.abs((y_true - y_pred) / y_true)),
        )
        self.assertEqual(
            rqm.get("mean_absolute_cum_error")(y_true, y_pred),
            mean_absolute_error(np.cumsum(y_true), np.cumsum(y_pred)),
        )
        self.assertEqual(
            rqm.get("median_absolute_cum_error")(y_true, y_pred),
            np.median(np.abs(np.cumsum(y_pred) - np.cumsum(y_true))),
        )
        self.assertEqual(
            rqm.get("mean_absolute_percentage_cum_error")(y_true, y_pred),
            np.mean(np.abs((np.cumsum(y_true) - np.cumsum(y_pred)) / np.cumsum(y_true))),
        )
        self.assertEqual(
            rqm.get("median_absolute_percentage_cum_error")(y_true, y_pred),
            np.median(np.abs((np.cumsum(y_true) - np.cumsum(y_pred)) / np.cumsum(y_true))),
        )
        self.assertEqual(
            rqm.get("mean_sign_cum_error")(y_true, y_pred),
            np.mean(np.sign(np.cumsum(y_true) - np.cumsum(y_pred))),
        )

        cqm = classification_quality_metrics

        self.assertTrue(np.isnan(cqm.get("accuracy")(y_true, y_pred)))
        self.assertTrue(np.isnan(cqm.get("precision")(y_true, y_pred)))
        self.assertTrue(np.isnan(cqm.get("recall")(y_true, y_pred)))

    def test_quality_metrics_with_bool_data(self):
        y_true = pd.Series([True, True, False])
        y_pred = pd.Series([True, False, False])
        rqm = regression_quality_metrics

        self.assertTrue(np.isnan(rqm.get("r2_score")(y_true, y_pred)))
        self.assertTrue(np.isnan(rqm.get("explained_variance_score")(y_true, y_pred)))
        self.assertTrue(np.isnan(rqm.get("mean_squared_error")(y_true, y_pred)))
        self.assertTrue(np.isnan(rqm.get("mean_error")(y_true, y_pred)))
        self.assertTrue(np.isnan(rqm.get("median_error")(y_true, y_pred)))
        self.assertTrue(np.isnan(rqm.get("mean_absolute_error")(y_true, y_pred)))
        self.assertTrue(np.isnan(rqm.get("median_absolute_error")(y_true, y_pred)))
        self.assertTrue(np.isnan(rqm.get("mean_absolute_percentage_error")(y_true, y_pred)))
        self.assertTrue(np.isnan(rqm.get("median_absolute_percentage_error")(y_true, y_pred)))
        self.assertTrue(np.isnan(rqm.get("mean_percentage_error")(y_true, y_pred)))
        self.assertTrue(np.isnan(rqm.get("median_percentage_error")(y_true, y_pred)))
        self.assertFalse(np.isnan(rqm.get("mean_absolute_cum_error")(y_true, y_pred)))
        self.assertFalse(np.isnan(rqm.get("median_absolute_cum_error")(y_true, y_pred)))
        self.assertFalse(np.isnan(rqm.get("mean_absolute_percentage_cum_error")(y_true, y_pred)))
        self.assertFalse(np.isnan(rqm.get("median_absolute_percentage_cum_error")(y_true, y_pred)))
        self.assertFalse(np.isnan(rqm.get("mean_sign_cum_error")(y_true, y_pred)))

        cqm = classification_quality_metrics

        self.assertAlmostEqual(cqm.get("accuracy")(y_true, y_pred), 0.6666, places=3)
        self.assertEqual(cqm.get("precision")(y_true, y_pred), 1)
        self.assertEqual(cqm.get("recall")(y_true, y_pred), 0.5)

    def test_r2_score(self):
        y_true = pd.Series([3])
        y_pred = pd.Series([2.5])
        self.assertTrue(np.isnan(regression_quality_metrics.get("r2_score")(y_true, y_pred)))

    def test_classification_metrics(self):
        cqm = classification_quality_metrics

        y_true = pd.Series([True])
        y_pred = pd.Series([True])
        self.assertEqual(cqm.get("accuracy")(y_true, y_pred), 1)
        self.assertEqual(cqm.get("accuracy")(y_true, y_pred), accuracy_score(y_true=y_true, y_pred=y_pred))
        self.assertEqual(cqm.get("precision")(y_true, y_pred), 1)
        self.assertEqual(cqm.get("precision")(y_true, y_pred), precision_score(y_true=y_true, y_pred=y_pred))
        self.assertEqual(cqm.get("recall")(y_true, y_pred), 1)
        self.assertEqual(cqm.get("recall")(y_true, y_pred), recall_score(y_true=y_true, y_pred=y_pred))

        y_true = pd.Series([False])
        y_pred = pd.Series([False])
        self.assertEqual(cqm.get("accuracy")(y_true, y_pred), 1)
        self.assertEqual(cqm.get("accuracy")(y_true, y_pred), accuracy_score(y_true=y_true, y_pred=y_pred))
        self.assertEqual(cqm.get("precision")(y_true, y_pred), 0)
        self.assertEqual(
            cqm.get("precision")(y_true, y_pred), precision_score(y_true=y_true, y_pred=y_pred, zero_division=0)
        )
        self.assertEqual(cqm.get("recall")(y_true, y_pred), 0)
        self.assertEqual(cqm.get("recall")(y_true, y_pred), recall_score(y_true=y_true, y_pred=y_pred, zero_division=0))

        y_true = pd.Series([1, 0])
        y_pred = pd.Series([0, 1])
        self.assertEqual(cqm.get("accuracy")(y_true, y_pred), 0)
        self.assertEqual(cqm.get("accuracy")(y_true, y_pred), accuracy_score(y_true=y_true, y_pred=y_pred))
        self.assertEqual(cqm.get("precision")(y_true, y_pred), 0)
        self.assertEqual(cqm.get("precision")(y_true, y_pred), precision_score(y_true=y_true, y_pred=y_pred))
        self.assertEqual(cqm.get("recall")(y_true, y_pred), 0)
        self.assertEqual(cqm.get("recall")(y_true, y_pred), recall_score(y_true=y_true, y_pred=y_pred))

        y_true = pd.Series([1, 1])
        y_pred = pd.Series([0, 1])
        self.assertEqual(cqm.get("accuracy")(y_true, y_pred), 0.5)
        self.assertEqual(cqm.get("accuracy")(y_true, y_pred), accuracy_score(y_true=y_true, y_pred=y_pred))
        self.assertEqual(cqm.get("precision")(y_true, y_pred), 1)
        self.assertEqual(cqm.get("precision")(y_true, y_pred), precision_score(y_true=y_true, y_pred=y_pred))
        self.assertEqual(cqm.get("recall")(y_true, y_pred), 0.5)
        self.assertEqual(cqm.get("recall")(y_true, y_pred), recall_score(y_true=y_true, y_pred=y_pred))

        y_true = pd.Series([0, 0])
        y_pred = pd.Series([0, 1])
        self.assertEqual(cqm.get("accuracy")(y_true, y_pred), 0.5)
        self.assertEqual(cqm.get("accuracy")(y_true, y_pred), accuracy_score(y_true=y_true, y_pred=y_pred))
        self.assertEqual(cqm.get("precision")(y_true, y_pred), 0)
        self.assertEqual(cqm.get("precision")(y_true, y_pred), precision_score(y_true=y_true, y_pred=y_pred))
        self.assertEqual(cqm.get("recall")(y_true, y_pred), 0)
        self.assertEqual(cqm.get("recall")(y_true, y_pred), recall_score(y_true=y_true, y_pred=y_pred, zero_division=0))

    def test_division_by_zero(self):
        y_true = pd.Series([0, 0, 0])
        y_pred = pd.Series([0, 0, 0])
        rqm = regression_quality_metrics

        self.assertTrue(np.isnan(rqm.get("mean_absolute_percentage_error")(y_true, y_pred)))
        self.assertTrue(np.isnan(rqm.get("median_absolute_percentage_error")(y_true, y_pred)))
        self.assertTrue(np.isnan(rqm.get("mean_percentage_error")(y_true, y_pred)))
        self.assertTrue(np.isnan(rqm.get("median_percentage_error")(y_true, y_pred)))
        self.assertTrue(np.isnan(rqm.get("mean_absolute_percentage_cum_error")(y_true, y_pred)))
        self.assertTrue(np.isnan(rqm.get("median_absolute_percentage_cum_error")(y_true, y_pred)))

        y_true = pd.Series([False, False, False])
        y_pred = pd.Series([False, False, False])
        rqm = regression_quality_metrics

        self.assertTrue(np.isnan(rqm.get("mean_absolute_percentage_error")(y_true, y_pred)))
        self.assertTrue(np.isnan(rqm.get("median_absolute_percentage_error")(y_true, y_pred)))
        self.assertTrue(np.isnan(rqm.get("mean_percentage_error")(y_true, y_pred)))
        self.assertTrue(np.isnan(rqm.get("median_percentage_error")(y_true, y_pred)))
        self.assertTrue(np.isnan(rqm.get("mean_absolute_percentage_cum_error")(y_true, y_pred)))
        self.assertTrue(np.isnan(rqm.get("median_absolute_percentage_cum_error")(y_true, y_pred)))
