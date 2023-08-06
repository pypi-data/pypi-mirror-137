# License: Apache-2.0
from typing import List, Tuple

import numpy as np

from ..util import util
from ._base_discretizer import _BaseBinning

EPSILON = 1e-10


from gators import DataFrame, Series


class IVBinning(_BaseBinning):
    """Bin the columns using quantile-based splits.

    The binning can be done inplace or by adding the binned
    columns to the existing data.

    Parameters
    ----------
    n_bins : int
        Number of bins to use.
    inplace : bool, default to False
        If False, return the dataframe with the new binned columns
        with the names "column_name__bin"). Otherwise, return
        the dataframe with the existing binned columns.

    Examples
    ---------
    >>> from gators.binning import IVBinning

    The binning can be done inplace by modifying the existing columns

    >>> obj = IVBinning(n_bins=3, inplace=True)

    or by adding new binned columns

    >>> obj = IVBinning(n_bins=3, inplace=True)

    The `fit`, `transform`, and `fit_transform` methods accept:

    * `dask` dataframes:

    >>> import dask.dataframe as dd
    >>> import pandas as pd
    >>> X = dd.from_pandas(pd.DataFrame({'A': [-1, 0, 1], 'B': [3, 2, 1]}), npartitions=1)

    * `koalas` dataframes:

    >>> import databricks.koalas as ks
    >>> X = ks.DataFrame({'A': [-1, 0, 1], 'B': [3, 2, 1]})

    * and `pandas` dataframes:

    >>> import pandas as pd
    >>> X = pd.DataFrame({'A': [-1, 0, 1], 'B': [3, 2, 1]})

    The result is a transformed dataframe belonging to the same dataframe library.

    * with `inplace=True`

    >>> obj = IVBinning(n_bins=3, inplace=True)
    >>> obj.fit_transform(X)
        A   B
    0  _0  _2
    1  _1  _1
    2  _2  _0

    * with `inplace=False`

    >>> X = pd.DataFrame({'A': [-1, 0, 1], 'B': [3, 2, 1]})
    >>> obj = IVBinning(n_bins=3, inplace=False)
    >>> obj.fit_transform(X)
       A  B A__bin B__bin
    0 -1  3     _0     _2
    1  0  2     _1     _1
    2  1  1     _2     _0

    Independly of the dataframe library used to fit the transformer, the `tranform_numpy` method only accepts NumPy arrays
    and returns a transformed NumPy array. Note that this transformer should **only** be used
    when the number of rows is small *e.g.* in real-time environment.

    >>> X = pd.DataFrame({'A': [-1, 0, 1], 'B': [3, 2, 1]})
    >>> obj.transform_numpy(X.to_numpy())
    array([[-1, 3, '_0', '_2'],
           [0, 2, '_1', '_1'],
           [1, 1, '_2', '_0']], dtype=object)

    See Also
    --------
    gators.binning.Binning
        Bin using equal splits.
    gators.binning.CustomBinning
        Bin using the variable quantiles.
    gators.binning.TreeBinning
        Bin using tree-based splits.
    """

    def __init__(
        self,
        n_bins: int,
        n_points: int = 100,
        regularization: float = 0.01,
        cutoff: float = 0.1,
        inplace=False,
    ):
        _BaseBinning.__init__(self, n_bins=n_bins, inplace=inplace)
        self.n_bins = n_bins
        self.regularization = regularization
        self.cutoff = cutoff
        self.n_points = n_points
        self.min_ratio = 0.1

    def compute_bins(
        self, X: DataFrame, y: Series
    ) -> Tuple[List[List[float]], np.ndarray]:
        """Compute the bins list and the bins array.
        The bin list is used for dataframes and
        the bins array is used for arrays.

        Parameters
        ----------
        X : DataFrame
            Input dataframe.
        n_bins : int
            Number of bins to use.

        Returns
        -------
        bins : List[List[float]]
            Bin splits definition.
            The dictionary keys are the column names to bin,
            its values are the split arrays.
        bins_np : np.ndarray
            Bin splits definition for NumPy.
        """
        bins = {}
        ivs = np.empty(self.n_points)
        # iq = X.quantile([0.01, 0.25, 0.75, 0.99])
        # iqr = iq.loc[0.75] - iq.loc[0.25]
        quantiles = X.quantile([0.01, 0.99])

        for col in X.columns:
            x = X[col]
            # TO IMPROVE (infs)
            # start = iq[col][0.25] if iqr[col] == 0 else  iq[col][0.01]
            # stop = iq[col][0.75] if iqr[col] == 0 else  iq[col][0.99]
            start = quantiles[col][0.01]
            stop = quantiles[col][0.99]
            val_vec = np.linspace(start, stop, self.n_points + 2)[1:-1]
            splits = np.array([-np.inf, np.inf])
            iv_list = [1e-2]
            for k in range(self.n_bins - 1):
                for i, val in enumerate(val_vec):
                    val_splits = np.sort(np.append(splits, val))
                    ivs[i] = self.compute_ivs(
                        x, y, val_splits, self.min_ratio, self.regularization
                    )
                splits = np.append(splits, val_vec[np.argmax(ivs)])
                val_vec = np.delete(val_vec, np.argmax(ivs))
                splits = np.sort(splits)
                bins[col] = splits
                iv_list.append(
                    self.compute_ivs(x, y, splits, self.min_ratio, self.regularization)
                )
                if (iv_list[-1] / iv_list[-2]) < 1.0 + self.cutoff:
                    break

        labels = {}
        for col in bins.keys():
            labels[col] = (
                [f"(-inf, {bins[col][1]}]"]
                + [f"({b1}, {b2}]" for b1, b2 in zip(bins[col][1:-2], bins[col][2:-1])]
                + [f"({bins[col][-2]}, inf)"]
            )
        bins_np = np.array([])
        return bins, bins_np, labels

    def compute_ivs(self, x, y, splits, min_ratio, regularization):
        iv = 0
        for l, r in zip(splits[:-1], splits[1:]):
            mask = (x > l) & (x <= r)
            if y[mask].mean() < min_ratio:
                iv += 0
                continue
            iv += self.compute_iv(y, mask, regularization)
        return iv

    @staticmethod
    def compute_iv(y_true, y_pred, regularization):
        ratio_1 = (y_true[y_pred == 1].sum() + regularization) / y_true.sum()
        ratio_0 = ((y_true[y_pred == 1] == 0).sum() + regularization) / (
            y_true == 0
        ).sum()
        iv = (ratio_1 - ratio_0) * np.log(ratio_1 / ratio_0)
        return iv
