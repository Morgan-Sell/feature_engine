# Authors: Morgan Sell <morganpsell@gmail.com>
# License: BSD 3 clause

import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin
from sklearn.utils.validation import check_is_fitted

from feature_engine.dataframe_checks import (
    _check_contains_inf,
    _check_contains_na,
    _check_input_matches_training_df,
    _is_dataframe,
)
from feature_engine.discretisation import (
    EqualFrequencyDiscretiser,
    EqualWidthDiscretiser
)
from feature_engine.encoding import MeanEncoder


class TargetMeanPredictor(BaseEstimator, ClassifierMixin, RegressorMixin):
    """

    Parameters
    ----------
    variable_type: str, default="categorical"
        Indicate whether the variable is categorical or numeric.

    bins: int, default=5
        If the dataset contains numerical variables, the number of bins into which
        the values will be sorted.

    strategy: str, default='equal_width'
        Whether to create the bins for discretization of numerical variables of
        equal width ('equal_width') or equal frequency ('equal_frequency').

    Attributes
    ----------


    Methods
    -------
    fit:

    predict:

    Notes
    -----


    See Also
    --------
    feature_engine.encoding.MeanEncoder
    feature_engine.discretisation.EqualWidthDiscretiser
    feature_engine.discretisation.EqualFrequencyDiscretiser

    References
    ----------


    """

    def __init__(
        self,
        regression: bool = True,
        bins: int = 5,
        strategy: str = "equal-width",
    ):
        # add check for 'variable_type' value - categorical or numeric
        # add check that 'variable_type' and 'strategy' comply
        #   - "categorical" and "mean-encoder" -> no bueno.
        #   - consider automating later

        self.regression = regression
        self.bins = bins
        self.strategy = strategy

    def fit(self, X: pd.DataFrame, y: pd.Series = None) -> pd.DataFrame:
        """
        Fit predictor per variables.

        Parameters
        ----------
        X : pandas dataframe of shape = [n_samples, n_features]
            The training input samples.

        y : pandas series of shape = [n_samples,]
            The target variable.
        """
        # check if dataframe
        _is_dataframe(X)

        # check for NaN values
        _check_contains_na(X)

        if not isinstance(y, pd.Series):
            y = pd.Series(y)


        if self.regression is True:
            pass





    def predict(self, X: pd.DataFrame) -> pd.Series:
        """

        Parameters
        ----------
        X : pandas dataframe of shape = [n_samples, n_features]
            The inputs uses to derive the predictions.

        Return
        -------
        y : pandas series of (n_samples,)
            Mean target values.

        """
        pass