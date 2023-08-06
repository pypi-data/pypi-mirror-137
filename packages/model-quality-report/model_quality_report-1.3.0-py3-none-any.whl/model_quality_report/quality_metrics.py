import numpy as np
import pandas as pd
from sklearn.metrics import (
    explained_variance_score,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    accuracy_score,
    precision_score,
    recall_score,
)


def _r2_score(y_true: pd.Series, y_pred: pd.Series) -> float:
    try:
        return r2_score(y_true=y_true, y_pred=y_pred)
    except (TypeError, ZeroDivisionError):
        return np.nan


def _explained_variance_score(y_true: pd.Series, y_pred: pd.Series) -> float:
    try:
        return explained_variance_score(y_true=y_true, y_pred=y_pred)
    except TypeError:
        return np.nan


def _mean_squared_error(y_true: pd.Series, y_pred: pd.Series) -> float:
    try:
        return mean_squared_error(y_true=y_true, y_pred=y_pred)
    except TypeError:
        return np.nan


def _mean_error(y_true: pd.Series, y_pred: pd.Series) -> float:
    try:
        return float(np.mean(y_true - y_pred))
    except TypeError:
        return np.nan


def _median_error(y_true: pd.Series, y_pred: pd.Series) -> float:
    try:
        return float(np.median(y_true - y_pred))
    except TypeError:
        return np.nan


def _mean_sign_error(y_true: pd.Series, y_pred: pd.Series) -> float:
    try:
        return float(np.mean(np.sign(y_true - y_pred)))
    except TypeError:
        return np.nan


def _mean_absolute_error(y_true: pd.Series, y_pred: pd.Series) -> float:
    try:
        return mean_absolute_error(y_true=y_true, y_pred=y_pred)
    except TypeError:
        return np.nan


def _median_absolute_error(y_true: pd.Series, y_pred: pd.Series) -> float:
    try:
        return float(np.median(np.abs(y_pred - y_true)))
    except TypeError:
        return np.nan


def _mean_percentage_error(y_true: pd.Series, y_pred: pd.Series) -> float:
    try:
        return float(np.mean((y_true - y_pred) / y_true))
    except (TypeError, ZeroDivisionError):
        return np.nan


def _median_percentage_error(y_true: pd.Series, y_pred: pd.Series) -> float:
    try:
        return float(np.median((y_true - y_pred) / y_true))
    except (TypeError, ZeroDivisionError):
        return np.nan


def _mean_absolute_percentage_error(y_true: pd.Series, y_pred: pd.Series) -> float:
    try:
        return float(np.mean(np.abs((y_true - y_pred) / y_true)))
    except (TypeError, ZeroDivisionError):
        return np.nan


def _median_absolute_percentage_error(y_true: pd.Series, y_pred: pd.Series) -> float:
    try:
        return float(np.median(np.abs((y_true - y_pred) / y_true)))
    except (TypeError, ZeroDivisionError):
        return np.nan


def _mean_absolute_cum_error(y_true: pd.Series, y_pred: pd.Series) -> float:
    try:
        return mean_absolute_error(y_true=np.cumsum(y_true), y_pred=np.cumsum(y_pred))
    except TypeError:
        return np.nan


def _median_absolute_cum_error(y_true: pd.Series, y_pred: pd.Series) -> float:
    try:
        return float(np.median(np.abs(np.cumsum(y_pred) - np.cumsum(y_true))))
    except TypeError:
        return np.nan


def _mean_absolute_percentage_cum_error(y_true: pd.Series, y_pred: pd.Series) -> float:
    try:
        return float(np.mean(np.abs((np.cumsum(y_true) - np.cumsum(y_pred)) / np.cumsum(y_true))))
    except (TypeError, ZeroDivisionError):
        return np.nan


def _median_absolute_percentage_cum_error(y_true: pd.Series, y_pred: pd.Series) -> float:
    try:
        return float(np.median(np.abs((np.cumsum(y_true) - np.cumsum(y_pred)) / np.cumsum(y_true))))
    except (TypeError, ZeroDivisionError):
        return np.nan


def _mean_sign_cum_error(y_true: pd.Series, y_pred: pd.Series) -> float:
    try:
        return float(np.mean(np.sign(np.cumsum(y_true) - np.cumsum(y_pred))))
    except TypeError:
        return np.nan


def _accuracy(y_true: pd.Series, y_pred: pd.Series) -> float:
    try:
        return accuracy_score(y_true=y_true, y_pred=y_pred, normalize=True)
    except ValueError:
        return np.nan


def _precision(y_true: pd.Series, y_pred: pd.Series) -> float:
    try:
        return precision_score(y_true=y_true, y_pred=y_pred, zero_division=0)
    except ValueError:
        return np.nan


def _recall(y_true: pd.Series, y_pred: pd.Series) -> float:
    try:
        return recall_score(y_true=y_true, y_pred=y_pred, zero_division=0)
    except ValueError:
        return np.nan


regression_quality_metrics = {
    "r2_score": _r2_score,
    "explained_variance_score": _explained_variance_score,
    "mean_squared_error": _mean_squared_error,
    "mean_error": _mean_error,
    "median_error": _median_error,
    "mean_sign_error": _mean_sign_error,
    "mean_absolute_error": _mean_absolute_error,
    "median_absolute_error": _median_absolute_error,
    "mean_percentage_error": _mean_percentage_error,
    "median_percentage_error": _median_percentage_error,
    "mean_absolute_percentage_error": _mean_absolute_percentage_error,
    "median_absolute_percentage_error": _median_absolute_percentage_error,
    "mean_absolute_cum_error": _mean_absolute_cum_error,
    "median_absolute_cum_error": _median_absolute_cum_error,
    "mean_absolute_percentage_cum_error": _mean_absolute_percentage_cum_error,
    "median_absolute_percentage_cum_error": _median_absolute_percentage_cum_error,
    "mean_sign_cum_error": _mean_sign_cum_error,
}

classification_quality_metrics = {"accuracy": _accuracy, "precision": _precision, "recall": _recall}


all_quality_metrics = {**regression_quality_metrics, **classification_quality_metrics}
