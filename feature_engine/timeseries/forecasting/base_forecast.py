# Authors: Morgan Sell <morganpsell@gmail.com>
# License: BSD 3 clause

from typing import Optional

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted

from feature_engine.dataframe_checks import (
    _check_contains_inf,
    _check_contains_na,
    _check_input_matches_training_df,
    _is_dataframe,
)
from feature_engine.docstrings import (
    Substitution,
    _feature_names_in_docstring,
    _fit_not_learn_docstring,
    _n_features_in_docstring,
    _missing_values_docstring,
    _drop_original_docstring,

)


@Substitution(
    missing_values=_missing_values_docstring,
    drop_original=_drop_original_docstring,
    feature_names_in_=_feature_names_in_docstring,
    fit=_fit_not_learn_docstring,
    n_features_in_=_n_features_in_docstring,
)
class BaseForecast(BaseEstimator, TransformerMixin):
    """
    Shared methods across time-series forecasting transformers.

    Parameters
    ----------
    {missing_values}

    {drop_original}

    Attributes
    ----------
    {feature_names_in_}

    {n_features_in_}
    """

    def __init__(
        self,
        missing_values: str = "raise",
        drop_original: bool = False,
    ) -> None:

        if missing_values not in ["raise", "ignore"]:
            raise ValueError(
                "missing_values takes only values 'raise' or 'ignore'. "
                f"Got {missing_values} instead."
            )

        if not isinstance(drop_original, bool):
            raise ValueError(
                "drop_original takes only boolean values True and False. "
                f"Got {drop_original} instead."
            )

        self.missing_values = missing_values
        self.drop_original = drop_original

    def _check_index(self, X: pd.DataFrame):
        """
        Check that the index does not have missing data and its values are unique.

        Parameters
        ----------
        X: pandas dataframe of shape = [n_samples, n_features]
            The training dataset.
        """
        if X.index.isnull().any():
            raise NotImplementedError(
                "The dataframe's index contains NaN values or missing data. "
                "Only dataframes with complete indexes are compatible with "
                "this transformer."
            )

        # Check that the index contains unique values.
        if X.index.is_unique is False:
            raise NotImplementedError(
                "The dataframe's index does not contain unique values. "
                "Only dataframes with unique values in the index are "
                "compatible with this transformer."
            )

        return self

    def _check_na_and_inf(self, X: pd.DataFrame):
        """
        Checks that the dataframe does not contain NaN or Infinite values.

        Parameters
        ----------
        X: pandas dataframe of shape = [n_samples, n_features]
            The dataset for training or transformation.
        """
        _check_contains_na(X, self.variables_)
        _check_contains_inf(X, self.variables_)

        return self

    def _check_trainset_features(self, X: pd.DataFrame):
        """
        Finds the number and name of the features in the training set.

        Parameters
        ----------
        X: pandas dataframe of shape = [n_samples, n_features]
            The dataset for training or transformation.
        """

        self.feature_names_in_ = X.columns.tolist()
        self.n_features_in_ = X.shape[1]

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Common checks performed before the feature transformation.

        Parameters
        ----------
        X: pandas dataframe of shape = [n_samples, n_features]
            The data to transform.

        Returns
        -------
        X: pandas dataframe of shape = [n_samples, n_features]
            The data to transform.
        """
        # checmk method fit has been called
        check_is_fitted(self)

        # check if 'X' is a dataframe
        X = _is_dataframe(X)

        # check if input data contains the same number of columns as the fitted
        # dataframe.
        _check_input_matches_training_df(X, self.n_features_in_)

        # Dataframes must have unique values in the index and no missing data.
        # Otherwise, when we merge the lag features we will duplicate rows.
        if X.index.isnull().sum() > 0:
            raise NotImplementedError(
                "The dataframe's index contains NaN values or missing data. "
                "Only dataframes with complete indexes are compatible with "
                "this transformer."
            )

        if X.index.is_unique is False:
            raise NotImplementedError(
                "The dataframe's index does not contain unique values. "
                "Only dataframes with unique values in the index are compatible "
                "with this transformer."
            )

        # check if dataset contains na
        if self.missing_values == "raise":
            _check_contains_na(X, self.variables_)
            _check_contains_inf(X, self.variables_)

        if self.sort_index is True:
            X.sort_index(inplace=True)

        return X
