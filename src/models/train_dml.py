
"""Double Machine Learning for synthetic pricing treatment effects."""

from pathlib import Path

import numpy as np
import pandas as pd
from econml.dml import LinearDML
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "data" / "prepared_pricing.csv"
OUTPUT_FILE = PROJECT_ROOT / "reports" / "dml_customer_effects.csv"

FEATURE_COLUMNS = [
    "age",
    "income",
    "past_purchases",
    "product_category",
]


def train_dml_model():
    """Fit DML and estimate customer-level treatment effects."""

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Prepared dataset not found: {DATA_FILE}. "
            "Run src/data_processing/prepare_pricing_data.py first."
        )

    df = pd.read_csv(DATA_FILE)

    required_columns = FEATURE_COLUMNS + [
        "customer_id",
        "treatment",
        "purchase",
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    if df.empty:
        raise ValueError("The prepared dataset is empty.")

    if df[required_columns].isnull().any().any():
        raise ValueError("Required columns contain missing values.")

    if set(df["treatment"].unique()) != {0, 1}:
        raise ValueError(
            "Treatment must contain both 0 (control) and 1 (discount)."
        )

    if not set(df["purchase"].unique()).issubset({0, 1}):
        raise ValueError("Purchase outcome must be binary (0 or 1).")

    # Customer characteristics used as model features.
    # Exclude purchase_probability to prevent target leakage.
    X = df[FEATURE_COLUMNS]

    treatment = df["treatment"].to_numpy(dtype=int)
    outcome = df["purchase"].to_numpy(dtype=float)

    # Encode the categorical product category.
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "category",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False,
                ),
                ["product_category"],
            ),
        ],
        remainder="passthrough",
    )

    X_encoded = preprocessor.fit_transform(X)
    X_encoded = np.asarray(X_encoded, dtype=float)

    # Configure the Linear Double Machine Learning model.
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
        fit_cate_intercept=False,
        cv=3,
        random_state=42,
    )

    # Fit using EconML's default inference configuration.
    model.fit(
        outcome,
        treatment,
        X=X_encoded,
        inference=None,
    )

    # Estimate discount versus control effects for each customer.
    effects = np.asarray(
        model.effect(X_encoded)
    ).reshape(-1)

    results = pd.DataFrame(
        {
            "customer_id": df["customer_id"],
            "estimated_discount_effect": effects,
        }
    )

    # Save customer-level treatment effect estimates.
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
