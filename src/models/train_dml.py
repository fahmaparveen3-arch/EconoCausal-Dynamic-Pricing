
"""Double Machine Learning for synthetic pricing treatment effects."""

from pathlib import Path

import numpy as np
import pandas as pd
from econml.dml import LinearDML
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "data" / "prepared_pricing.csv"
OUTPUT_FILE = PROJECT_ROOT / "reports" / "dml_customer_effects.csv"

FEATURE_COLUMNS = [
    "age",
    "income",
    "past_purchases",
    "product_category",
]

REQUIRED_COLUMNS = FEATURE_COLUMNS + [
    "customer_id",
    "treatment",
    "purchase",
]


def validate_dml_data(df):
    """Validate the dataset required for DML modelling."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input data must be a pandas DataFrame.")

    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    if df.empty:
        raise ValueError("The prepared dataset is empty.")

    if df[REQUIRED_COLUMNS].isnull().any().any():
        raise ValueError("Required columns contain missing values.")

    if df["customer_id"].duplicated().any():
        raise ValueError("Customer IDs must be unique.")

    if not set(df["treatment"].unique()).issubset({0, 1}):
        raise ValueError("Treatment must contain only 0 and 1.")

    if set(df["treatment"].unique()) != {0, 1}:
        raise ValueError(
            "Treatment must contain both 0 (control) and 1 (discount)."
        )

    if not set(df["purchase"].unique()).issubset({0, 1}):
        raise ValueError("Purchase outcome must be binary (0 or 1).")

    if df["purchase"].nunique() != 2:
        raise ValueError(
            "Purchase outcome must contain both 0 and 1."
        )

    numeric_columns = ["age", "income", "past_purchases"]

    for column in numeric_columns:
        values = pd.to_numeric(df[column], errors="raise").to_numpy(
            dtype=float
        )
        if not np.isfinite(values).all():
            raise ValueError(
                f"Column '{column}' contains non-finite values."
            )

    if (df["age"] < 18).any() or (df["age"] > 70).any():
        raise ValueError("Age must be between 18 and 70.")

    if (df["income"] < 0).any():
        raise ValueError("Income cannot be negative.")

    if (df["past_purchases"] < 0).any():
        raise ValueError("Past purchases cannot be negative.")


def fit_dml_model(df):
    """Fit DML and return the model and customer-level effects."""
    validate_dml_data(df)

    # Use customer characteristics, not generated outcomes or probabilities.
    X = df[FEATURE_COLUMNS].copy()
    treatment = df["treatment"].to_numpy(dtype=int)
    outcome = df["purchase"].to_numpy(dtype=float)

    # Encode product category and retain numerical customer features.

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "category",
                OneHotEncoder(
                    drop="first",
                    handle_unknown="ignore",
                    sparse_output=False,
                ),
                ["product_category"],
            ),
        ],
        remainder="passthrough",
    )


    X_encoded = np.asarray(
        preprocessor.fit_transform(X),
        dtype=float,
    )

    model = LinearDML(
        model_y=RandomForestRegressor(
            n_estimators=100,
            min_samples_leaf=20,
            random_state=42,
            n_jobs=-1,
        ),
        model_t=RandomForestClassifier(
            n_estimators=100,
            min_samples_leaf=20,
            random_state=42,
            n_jobs=-1,
        ),
        discrete_treatment=True,
        fit_cate_intercept=True,
        cv=3,
        random_state=42,
    )

    model.fit(
        outcome,
        treatment,
        X=X_encoded,
        inference=None,
    )

    effects = np.asarray(model.effect(X_encoded)).reshape(-1)

    if len(effects) != len(df):
        raise RuntimeError(
            "The number of estimated effects does not match the data."
        )

    if not np.isfinite(effects).all():
        raise ValueError("Estimated treatment effects are not finite.")

    results = pd.DataFrame(
        {
            "customer_id": df["customer_id"].to_numpy(),
            "estimated_discount_effect": effects,
        }
    )

    return model, results

def evaluate_dml_holdout(df, test_size=0.25):
    """Evaluate DML effects on customers excluded from model fitting."""

    validate_dml_data(df)

    train_df, test_df = train_test_split(
        df,
        test_size=test_size,
        random_state=42,
        stratify=df["treatment"],
    )

    # Fit preprocessing using training customers only.
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "category",
                OneHotEncoder(
                    drop="first",
                    handle_unknown="ignore",
                    sparse_output=False,
                ),
                ["product_category"],
            ),
        ],
        remainder="passthrough",
    )

    X_train = preprocessor.fit_transform(train_df[FEATURE_COLUMNS])
    X_test = preprocessor.transform(test_df[FEATURE_COLUMNS])

    model = LinearDML(
        model_y=RandomForestRegressor(
            n_estimators=100,
            min_samples_leaf=20,
            random_state=42,
            n_jobs=-1,
        ),
        model_t=RandomForestClassifier(
            n_estimators=100,
            min_samples_leaf=20,
            random_state=42,
            n_jobs=-1,
        ),
        discrete_treatment=True,
        fit_cate_intercept=True,
        cv=3,
        random_state=42,
    )

    model.fit(
        train_df["purchase"].to_numpy(dtype=float),
        train_df["treatment"].to_numpy(dtype=int),
        X=np.asarray(X_train, dtype=float),
        inference=None,
    )

    test_effects = np.asarray(
        model.effect(np.asarray(X_test, dtype=float))
    ).reshape(-1)

    if not np.isfinite(test_effects).all():
        raise ValueError("Holdout effects contain non-finite values.")

    return pd.DataFrame({
        "customer_id": test_df["customer_id"].to_numpy(),
        "estimated_discount_effect": test_effects,
    })



def train_dml_model():
    """Load data, fit DML, and save customer-level effects."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Prepared dataset not found: {DATA_FILE}. "
            "Run src.data_processing.prepare_pricing_data first."
        )

    df = pd.read_csv(DATA_FILE)
    model, results = fit_dml_model(df)

    effects = results["estimated_discount_effect"].to_numpy()

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(OUTPUT_FILE, index=False)

    print("\nDML model trained successfully!")
    print("Rows used:", len(df))
    print(
        "Average estimated treatment effect:",
        round(float(np.mean(effects)), 6),
    )
    print(
        "Minimum estimated effect:",
        round(float(np.min(effects)), 6),
    )
    print(
        "Maximum estimated effect:",
        round(float(np.max(effects)), 6),
    )
    print("Saved customer effects to:", OUTPUT_FILE)

    return model, results


if __name__ == "__main__":
    train_dml_model()
