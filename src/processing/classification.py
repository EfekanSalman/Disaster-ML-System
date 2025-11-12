import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


# This is our "clean" system component for Problem 2 (Classification).
# Its Single Responsibility: To take raw data and clean it
# based on the 'Disaster Subgroup' target (y).


class SubgroupDataPreprocessor(BaseEstimator, TransformerMixin):
    """
    A Scikit-learn pipeline component that processes raw data
    for a classification task.

    Operations performed:
    1. Removes rows that have NaN values in the target variable ('Disaster Subgroup').

    IMPORTANT: Unlike the class in Problem 1, this class DOES NOT TOUCH
    'Total Damages' or the 'Log' transformation.

    This allows us to use (more) data where 'Total Damages' is NaN
    but the 'Subgroup' is known.
    """

    def __init__(self, target_col: str = "Disaster Subgroup"):
        self.target_col = target_col

        # This class DOES NOT need to know which features (X)
        # we will use, unlike in Problem 1.
        # We will make this decision in the 'notebook' (prototyping)
        # or the 'ColumnTransformer' (system).

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        # We learn nothing
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        # Take a copy of X
        df = X.copy()

        # 1. Prepare the Target Variable (Subgroup)

        # Keep only the rows where the target (Subgroup) is known
        # (Based on our EDA, this is almost all the data)
        df = df.dropna(subset=[self.target_col])

        # 2. Return the rest of the raw data (including all X features)
        # in the filtered form

        return df
