import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


# REFACTORED CLASS
# This class now has a SINGLE RESPONSIBILITY:
# To process the target variable (Total Damages) and
# select the rows suitable for model training.
# It will no longer TOUCH the X features.


class DamageDataPreprocessor(BaseEstimator, TransformerMixin):
    """
    A component that prepares the REQUIRED ROWS and the TARGET VARIABLE
    to ready the dataset for model training.

    Operations performed:
    1. Removes rows that have NaN values in the target variable (Total Damages).
    2. Removes rows where the target is not greater than 0 (We will take the Log).
    3. Transforms the target variable (y) to Log10 and stores it as 'Log_Total_Damages'.

    IMPORTANT: It no longer touches the features (X).
    The ColumnTransformer will handle this task.
    """

    def __init__(self, target_col: str = "Total Damages ('000 US$)"):
        self.target_col = target_col
        self.log_target_col = "Log_Total_Damages"  # Our new target

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        # We learn nothing
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        # Take a copy of X so we don't mess up the original data
        df = X.copy()

        # 1. Prepare the Target Variable (Total Damages)

        # Keep only the rows with damage data (Prototyping Step 1)
        df = df.dropna(subset=[self.target_col])

        # Only take values greater than 0 (Avoid taking the log of non-positive numbers)
        df = df[df[self.target_col] > 0]

        # Perform Log transformation (Prototyping Step 1)
        df[self.log_target_col] = np.log10(df[self.target_col])

        # 2. FEATURE PROCESSING SECTION REMOVED
        # No filling with 'Missing'.
        # This will ensure that the ColumnTransformer's numerical 'SimpleImputer'
        # works correctly.

        # Return the entire DataFrame
        return df
