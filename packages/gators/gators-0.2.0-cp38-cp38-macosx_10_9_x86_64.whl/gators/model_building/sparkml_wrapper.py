# License: Apache-2.0
from sklearn.base import BaseEstimator


from ..util import util


class SparkMLWrapper(BaseEstimator):
    """SparkML wrapper class.

    Examples
    --------
    >>> import numpy as np
    >>> import xgboost as xgb
    >>> from gators.model_building import XGBBoosterBuilder
    >>> X_train = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    >>> y_train = np.array([0, 1, 1, 0])
    >>> model = xgb.XGBClassifier(eval_metric='logloss').fit(X_train, y_train)
    >>> xgbooster = XGBBoosterBuilder.train(
    ... model=model,
    ... X_train=X_train,
    ... y_train=y_train)
    >>> xgbooster.predict(xgb.DMatrix(X_train))
    array([0.5, 0.5, 0.5, 0.5], dtype=float32)

    """

    def __init__(self, spark_model):
        """Convert the XGBoost model to a XGB Booster model.

        Parameters
        ----------
        model : Union[XGBClassifier, XGBRegressor, XGBRFClassifier, XGBRFRegressor]
            Trained xgboost.sklearn model.
        X_train : np.ndarray
            Train array.
        y_train : np.ndarray
             Target values.

        Returns
        -------
        xgboost.Booster
            Trained xgboost Booster model.
        """

    def fit(self, X, y):
        self.model = util.fit_spark_ml(self.model, X, y)

    def predict(self, X):
        self.model.predict


# from pyspark.ml.classification import RandomForestClassifier as RFCSpark

# @pytest.fixture
# def data_ks():
#     X = ks.DataFrame(
#         {
#             "A": [22.0, 38.0, 26.0, 35.0, 35.0, 28.11, 54.0, 2.0, 27.0, 14.0],
#             "B": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
#             "C": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
#         }
#     )
#     y = ks.Series([0, 1, 1, 1, 0, 0, 0, 0, 1, 1], name="TARGET")
#     X_expected = X[["A"]].copy()
#     model = RFCSpark(numTrees=1, maxDepth=2, labelCol=y.name, seed=0)
#     obj = SelectFromModel(model=model, k=2).fit(X, y)
#     return obj, X, X_expected
