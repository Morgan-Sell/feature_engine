# Authors: Soledad Galli <solegalli@protonmail.com>
# License: BSD 3 clause

from typing import List, Union

import pandas as pd

from feature_engine.docstrings import (
    Substitution,
    _fit_transform_docstring,
    _inverse_transform_docstring,
    _n_features_in_docstring,
    _variables_attribute_docstring,
)
from feature_engine.encoding._docstrings import (
    _errors_docstring,
    _ignore_format_docstring,
    _transform_docstring,
    _variables_docstring,
)
from feature_engine.encoding.base_encoder import BaseCategorical


@Substitution(
    ignore_format=_ignore_format_docstring,
    variables=_variables_docstring,
    errors=_errors_docstring,
    variables_=_variables_attribute_docstring,
    n_features_in_=_n_features_in_docstring,
    fit_transform=_fit_transform_docstring,
    transform=_transform_docstring,
    inverse_transform=_inverse_transform_docstring,
)
class MeanEncoder(BaseCategorical):
    """
    The MeanEncoder() replaces categories by the mean value of the target for each
    category.

    For example in the variable colour, if the mean of the target for blue, red
    and grey is 0.5, 0.8 and 0.1 respectively, blue is replaced by 0.5, red by 0.8
    and grey by 0.1.

    The encoder will encode only categorical variables by default (type 'object' or
    'categorical'). You can pass a list of variables to encode. Alternatively, the
    encoder will find and encode all categorical variables (type 'object' or
    'categorical').

    With `ignore_format=True` you have the option to encode numerical variables as well.
    The procedure is identical, you can either enter the list of variables to encode, or
    the transformer will automatically select all variables.

    The encoder first maps the categories to the numbers for each variable (fit). The
    encoder then replaces the categories with those numbers (transform).

    More details in the :ref:`User Guide <mean_encoder>`.

    Parameters
    ----------
    {variables}

    {ignore_format}

    {errors}

    Attributes
    ----------
    encoder_dict_:
        Dictionary with the target mean value per category per variable.

    {variables_}

    {n_features_in_}

    Methods
    -------
    fit:
        Learn the target mean value per category, per variable.

    {transform}

    {fit_transform}

    {inverse_transform}

    Notes
    -----
    NAN are introduced when encoding categories that were not present in the training
    dataset. If this happens, try grouping infrequent categories using the
    RareLabelEncoder().

    Check also the related transformers in the the open-source package
    `Category encoders <https://contrib.scikit-learn.org/category_encoders/>`_

    See Also
    --------
    feature_engine.encoding.RareLabelEncoder
    category_encoders.target_encoder.TargetEncoder
    category_encoders.m_estimate.MEstimateEncoder

    References
    ----------
    .. [1] Micci-Barreca D. "A Preprocessing Scheme for High-Cardinality Categorical
       Attributes in Classification and Prediction Problems". ACM SIGKDD Explorations
       Newsletter, 2001. https://dl.acm.org/citation.cfm?id=507538
    """

    def __init__(
        self,
        variables: Union[None, int, str, List[Union[str, int]]] = None,
        ignore_format: bool = False,
        errors: str = "ignore",
    ) -> None:

        super().__init__(variables, ignore_format, errors)

    def fit(self, X: pd.DataFrame, y: pd.Series):
        """
        Learn the mean value of the target for each category of the variable.

        Parameters
        ----------
        X: pandas dataframe of shape = [n_samples, n_features]
            The training input samples. Can be the entire dataframe, not just the
            variables to be encoded.

        y: pandas series
            The target.
        """

        X = self._check_fit_input_and_variables(X)

        if not isinstance(y, pd.Series):
            y = pd.Series(y)

        temp = pd.concat([X, y], axis=1)
        temp.columns = list(X.columns) + ["target"]

        self.encoder_dict_ = {}

        for var in self.variables_:
            self.encoder_dict_[var] = temp.groupby(var)["target"].mean().to_dict()

        self._check_encoding_dictionary()

        self.n_features_in_ = X.shape[1]

        return self

    # Ugly work around to import the docstring for Sphinx, otherwise not necessary
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = super().transform(X)

        return X

    transform.__doc__ = BaseCategorical.transform.__doc__

    def inverse_transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = super().inverse_transform(X)

        return X

    inverse_transform.__doc__ = BaseCategorical.inverse_transform.__doc__
