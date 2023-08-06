from typing import List

import pandas as pd

from model_quality_report.quality_report.base import QualityReportBase


class RegressionQualityReport(QualityReportBase):
    def _calculate_quality_metrics_as_pandas(self, y_true: pd.Series, y_pred: pd.Series) -> pd.Series:
        return (
            pd.Series(self._calculate_quality_metrics(y_true=y_true, y_pred=y_pred))
            .rename(self.lbl_metric_value)
            .rename_axis(self.lbl_metrics, axis=0)
            .reset_index()
        )

    def _convert_list_of_data_to_pandas(self, data: List[pd.Series], name: str = None) -> pd.Series:
        return pd.Series(data[0], name=name)
