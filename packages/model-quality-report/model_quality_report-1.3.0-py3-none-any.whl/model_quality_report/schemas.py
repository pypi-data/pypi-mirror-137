from pandera import SchemaModel
from pandera.typing import Series, Float, String, Bool


class ModelQualityMetricsSchema(SchemaModel):
    metrics: Series[String]
    value: Series[Float]


class TrueAndPredictedFloatSchema(SchemaModel):
    true: Series[Float]
    predicted: Series[Float]


class TrueAndPredictedBoolSchema(SchemaModel):
    true: Series[Bool]
    predicted: Series[Bool]
