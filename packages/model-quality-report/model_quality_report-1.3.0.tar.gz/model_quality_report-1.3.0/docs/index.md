# Model Quality Report

## Metrics

The following metrics are computed as a result of model evaluation:

- Regression metrics:
    - explained_variance_score: [sklearn doc](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.explained_variance_score.html)
    - mean_squared_error: [sklearn doc](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html)
    - r2_score: [sklearn doc](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html)
    - mean_error: $\text{mean}\left(y_{true}-y_{pred}\right)$
    - median_error: $\text{med}\left(y_{true}-y_{pred}\right)$
    - mean_sign_error: $\text{mean}\left(\text{sign}\left(y_{true}-y_{pred}\right)\right)$
    - mean_absolute_error: [sklearn doc](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_absolute_error.html)
    - median_absolute_error: $\text{med}\left|y_{true}-y_{pred}\right|$
    - mean_percentage_error: $\text{mean}\left(\left(y_{true}-y_{pred}\right)/y_{true}\right)$
    - median_percentage_error: $\text{med}\left(\left(y_{true}-y_{pred}\right)/y_{true}\right)$
    - mean_absolute_percentage_error: $\text{mean}\left|\left(y_{true}-y_{pred}\right)/y_{true}\right|$
    - median_absolute_percentage_error: $\text{med}\left|\left(y_{true}-y_{pred}\right)/y_{true}\right|$

- Cumulative metrics:
    - mean of signs of cumulative error: $\text{mean}\left(\text{sign}\left(\tilde{y}_{true}-\tilde{y}_{pred}\right)\right)$
    - mean absolute cumulative error: $\text{mean}\left|\tilde{y}_{true}-\tilde{y}_{pred}\right|$
    - median absolute cumulative error: $\text{med}\left|\tilde{y}_{true}-\tilde{y}_{pred}\right|$
    - mean absolute percentage cumulative error: $\text{mean}\left|\left(\tilde{y}_{true}-\tilde{y}_{pred}\right)/\tilde{y}_{true}\right|$
    - median absolute percentage cumulative error: $\text{med}\left|\left(\tilde{y}_{true}-\tilde{y}_{pred}\right)/\tilde{y}_{true}\right|$
  
    where $\tilde{y}=(\tilde{y}^t)_{t=1,\ldots,T}$ is the vector of cumulative values of $y_t$. To be precise, $\tilde{y}^t=\overset{t}{\underset{s=1}{\sum}} y_s$.

- Classification metrics:
    - accuracy: [sklearn doc](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html)
    - precision: [sklearn doc](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html)
    - recall: [sklearn doc](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html)
