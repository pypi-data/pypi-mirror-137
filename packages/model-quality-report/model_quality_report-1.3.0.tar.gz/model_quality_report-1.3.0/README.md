[![Documentation Status](https://readthedocs.org/projects/model-quality-report/badge/?version=latest&style=flat-square)](https://model-quality-report.readthedocs.io/en/latest/?badge=latest)

# Model Quality Report

This packages enables a quick creation of a model quality report, which is returned 
as a `dict`. 

Main ingredients are a data splitter creating test and training data according various rules and the quality report itself. The quality report takes care of the splitting, fitting, predicting and finally deriving quality metrics.  

## Documentation

The official documentation is hosted on ReadTheDocs: [https://model-quality-report.readthedocs.io](https://model-quality-report.readthedocs.io)

## Installing the package

Latest available code:
```shell
pip install model_quality_report
```
Specific version:
```shell
pip install model_quality_report==X.Y.Z
```

## Quickstart

* The `RandomDataSplitter` splits data randomly using `sklearn.model_selection.train_test_split`:
```python
X = pd.DataFrame({'a': [1, 2, 3, 4, 5], 'b': ['a', 'b', 'c', 'd', 'e']})
y = pd.Series(data=range(5))

splitter = RandomDataSplitter(test_size=0.33, random_state=2)
X_train, X_test, y_train, y_test = splitter.split(X, y)
```

* The `TimeDeltaDataSplitter` divides such that data from last period of length `time_delta` is used as test data. Here a `pd.Timedelta` and the date column name is provided:
```python
splitter = TimeDeltaDataSplitter(date_column_name='shipping_date', time_delta=pd.Timedelta(3, unit='h')) 
X_train, X_test, y_train, y_test = splitter.split(X, y)
```

* The `SplitDateDataSplitter` splits such that data after a provided date are used as test data. Additionally, the name of the date column has to be provided:
```python
splitter = SplitDateDataSplitter(date_column_name='shipping_date', split_date=pd.Timstamp('2016-01-01'))
X_train, X_test, y_train, y_test = splitter.split(X, y)
```

* The `SortedDataSplitter` requires a column with sortable values. Data are divided such that the test data set encompasses last fraction `test_size`. Sorting can be in ascending and descending order. 
```python
splitter = SortedDataSplitter(sortable_column_name='shipping_date', test_size=0.2, ascending=True)
X_train, X_test, y_train, y_test = splitter.split(X, y)
```

* Using `RegressionQualityReport` class a quality report for a regression model can be created as following:

```python
splitter = SplitDateDataSplitter(date_column_name='shipping_date', split_date=pd.Timstamp('2016-01-01'))
model = sklearn.linear_model.LinearRegression()
quality_reporter = RegressionQualityReport(model, splitter)
report = quality_reporter.create_reports()
```
An exemplary report looks as follows:
```python
{'metrics': 
    {'explained_variance_score': -6.018595041322246, 
     'mape': 0.3863636363636345, 
     'mean_absolute_error': 4.242424242424224, 
     'mean_squared_error': 29.426997245178825, 
     'median_absolute_error': 2.272727272727268, 
     'r2_score': -10.03512396694206}, 
 'data': 
    {'true': {3: 10, 4: 12, 2: 8}, 
     'predicted': {3: 12.272727272727268, 4: 20.999999999999964, 2: 6.545454545454561}}}  
```
Note that the `model` must have a `model.fit` and a `model.predict` function.

## Available Features

**Data Splitter**

`RandomDataSplitter`: splits randomly
`TimeDeltaDataSplitter`: uses data in last period of length as test data
`SplitDateDataSplitter`: uses data with timestamp newer than split date as test data
`SortedDataSplitter`: sorts data along given column and takes last fraction of size x_test as test data
`ByHorizon`: produces a list of splits of temporal data such that each consecutive train set has one more observation and test set one less
`ByFrequency`: produces a list of splits of temporal data such that the data is split by a series of dates on a specified frequency
`FixedDates`: produces a list of splits of temporal data given a list of fixed dates.

**Quality Report**

`RegressionQualityReport`: creates a quality report for a regression model
`CrossValidationTimeSeriesQualityReport`: creates a quality report for a time series model

**Report Aggregation**

- `ModelComparisonReport` aggregates reports using the list of derivatives of `QualityReportBase`, data, and experiment keys.
- `ReportAggregator` is designed to aggregate model quality reports from different models that potentially use different input/output data and can not fit into the framework of `ModelComparisonReport`. `ReportAggregator` operates with the list of classes that derive from `ExperimentBase`.  

## Developers should know

Create a virtual environment and activate it
```shell
python -m venv venv
source venv/bin/activate
```
Install the development packages
```shell
pip install -e .[dev]
```
and use pre-commit to make sure that your code is blackified automatically (used the `black` package):
```shell
pre-commit install
```
Run tests:
```shell
pip install -e .[test]
coverage run -m unittest discover tests
coverage report
```
Build documentation (see more details [here](https://www.mkdocs.org/#getting-started)):
```shell
pip install -e .[doc]
mkdocs build
```
or use
```shell
mkdocs serve
```
if you prefer a live, self-refreshing, documentation.
