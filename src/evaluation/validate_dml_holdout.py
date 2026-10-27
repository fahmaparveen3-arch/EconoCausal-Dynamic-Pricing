
"""Validate holdout DML estimates against synthetic ground truth."""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from src.models.train_dml import evaluate_dml_holdout


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "data" / "prepared_pricing.csv"
REPORT_FILE = PROJECT_ROOT / "reports" / "dml_holdout_validation.csv"

DISCOUNT_LEVELS = [0.05, 0.10, 0.15, 0.20]


def calculate_purchase_probability(df, discount_rate):
    """Recreate the synthetic generator's purchase probability."""

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

    log_odds = baseline_log_odds + discount_sensitivity * discount_rate

    return 1 / (1 + np.exp(-log_odds))


def main():
    df = pd.read_csv(DATA_FILE)

    # Recreate the same 25% holdout split used by evaluate_dml_holdout.
    _, test_df = train_test_split(
        df,
        test_size=0.25,
        random_state=42,
        stratify=df["treatment"],
    )

    # Estimate effects only for the held-out customers.
    estimates = evaluate_dml_holdout(df)

    merged = test_df[["customer_id", "age", "income",
                      "past_purchases", "product_category"]].merge(
        estimates,
        on="customer_id",
        how="inner",
        validate="one_to_one",
    )

    probability_no_discount = calculate_purchase_probability(merged, 0.0)

    counterfactual_effects = []

    for rate in DISCOUNT_LEVELS:
        probability_with_discount = calculate_purchase_probability(
            merged, rate
        )
        counterfactual_effects.append(
            probability_with_discount - probability_no_discount
        )

    true_effect = np.mean(counterfactual_effects, axis=0)
    estimated_effect = merged["estimated_discount_effect"].to_numpy()

    report = pd.DataFrame({
        "customer_id": merged["customer_id"],
        "true_policy_effect": true_effect,
        "estimated_dml_effect": estimated_effect,
        "absolute_error": np.abs(estimated_effect - true_effect),
    })

    true_ate = float(np.mean(true_effect))
    estimated_ate = float(np.mean(estimated_effect))
    bias = estimated_ate - true_ate
    mae = float(np.mean(np.abs(estimated_effect - true_effect)))
    rmse = float(np.sqrt(np.mean((estimated_effect - true_effect) ** 2)))

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(REPORT_FILE, index=False)

    print("\nDML Holdout Validation")
    print("----------------------")
    print(f"Customers evaluated: {len(report)}")
    print(f"True policy ATE:     {true_ate:.6f}")
    print(f"Estimated DML ATE:   {estimated_ate:.6f}")
    print(f"ATE estimation bias: {bias:.6f}")
    print(f"Individual-effect MAE:  {mae:.6f}")
    print(f"Individual-effect RMSE: {rmse:.6f}")
    print(f"\nReport saved to: {REPORT_FILE}")


if __name__ == "__main__":
    main()
