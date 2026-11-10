"""Validate DML performance across different train/test split ratios."""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from src.models.train_dml import evaluate_dml_holdout


ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = ROOT / "data" / "prepared_pricing.csv"
REPORT_FILE = ROOT / "reports" / "dml_split_ratio_validation.csv"

TEST_RATIOS = [0.30, 0.25, 0.20]
DISCOUNTS = [0.05, 0.10, 0.15, 0.20]
SEED = 42


def true_purchase_probability(df, discount):
    """Recreate the synthetic data generator's purchase probability."""

    baseline_log_odds = (
        -2.0
        + 0.025 * (df["age"] - 40)
        + 0.000015 * (df["income"] - 45000)
        + 0.12 * df["past_purchases"]
        + 0.20 * (df["product_category"] == "Beauty")
        - 0.15 * (df["product_category"] == "Electronics")
    )

    discount_sensitivity = (
        3.0
        + 0.08 * df["past_purchases"]
        + 0.00001 * (df["income"] - 45000)
    )

    log_odds = baseline_log_odds + discount_sensitivity * discount

    return 1 / (1 + np.exp(-log_odds))


def calculate_true_effect(df, discount_weights):
    """Calculate the true average policy effect for each customer."""

    control_probability = true_purchase_probability(df, 0.0)

    effects = [
        true_purchase_probability(df, rate) - control_probability
        for rate in DISCOUNTS
    ]

    return np.average(
        np.column_stack(effects),
        axis=1,
        weights=discount_weights,
    )


def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

    df = pd.read_csv(DATA_FILE)
    treated_rates = df.loc[df["treatment"] == 1, "discount_rate"]
    counts = treated_rates.value_counts()
    missing_levels = set(DISCOUNTS) - set(counts.index)

    if missing_levels:
        raise ValueError(f"Missing discount levels: {sorted(missing_levels)}")

    discount_weights = (
        counts.reindex(DISCOUNTS).to_numpy(dtype=float)
        / len(treated_rates)
    )

    results = []

    for test_ratio in TEST_RATIOS:
        print(f"\nEvaluating {int((1-test_ratio)*100)}/{int(test_ratio*100)} split...")

        # Recreate the same holdout split used by the DML function.
        _, test_df = train_test_split(
            df,
            test_size=test_ratio,
            random_state=SEED,
            stratify=df["treatment"],
        )

        # Estimate effects using training customers only.
        estimates = evaluate_dml_holdout(df, test_size=test_ratio)

        # Match estimates to the corresponding holdout customers.
        merged = test_df[
            [
                "customer_id",
                "age",
                "income",
                "past_purchases",
                "product_category",
            ]
        ].merge(
            estimates,
            on="customer_id",
            how="left",
            validate="one_to_one",
        )

        if len(merged) != len(test_df):
            raise ValueError("Holdout customer matching failed.")

        if merged["estimated_discount_effect"].isna().any():
            raise ValueError("Some holdout estimates are missing.")

        true_effect = calculate_true_effect(merged, discount_weights)
        estimated_effect = merged[
            "estimated_discount_effect"
        ].to_numpy()

        errors = estimated_effect - true_effect

        if not np.isfinite(errors).all():
            raise ValueError("Validation errors contain non-finite values.")

        true_ate = float(np.mean(true_effect))
        estimated_ate = float(np.mean(estimated_effect))
        bias = estimated_ate - true_ate

        results.append({
            "training_percentage": int((1 - test_ratio) * 100),
            "testing_percentage": int(test_ratio * 100),
            "training_customers": len(df) - len(test_df),
            "holdout_customers": len(test_df),
            "true_ate": true_ate,
            "estimated_ate": estimated_ate,
            "ate_bias": bias,
            "absolute_ate_bias": abs(bias),
            "mae": float(np.mean(np.abs(errors))),
            "rmse": float(np.sqrt(np.mean(errors ** 2))),
        })

    report = pd.DataFrame(results)

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(REPORT_FILE, index=False)

    print("\nDML Train/Test Split Validation")
    print("--------------------------------")
    print(report.to_string(
        index=False,
        float_format=lambda value: f"{value:.6f}",
    ))
    print(f"\nReport saved to: {REPORT_FILE}")


if __name__ == "__main__":
    main()
