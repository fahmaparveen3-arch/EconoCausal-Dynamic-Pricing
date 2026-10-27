
"""Validate DML estimates against the known synthetic treatment effect."""

from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = PROJECT_ROOT / "data" / "prepared_pricing.csv"
EFFECTS_FILE = PROJECT_ROOT / "reports" / "dml_customer_effects.csv"
REPORT_FILE = PROJECT_ROOT / "reports" / "dml_truth_validation.csv"

DISCOUNT_LEVELS = [0.05, 0.10, 0.15, 0.20]


def calculate_purchase_probability(df, discount_rate):
    """Recreate the generator's purchase probability formula."""

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
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

    if not EFFECTS_FILE.exists():
        raise FileNotFoundError(f"DML effects not found: {EFFECTS_FILE}")

    df = pd.read_csv(DATA_FILE)
    effects = pd.read_csv(EFFECTS_FILE)

    if df["customer_id"].duplicated().any():
        raise ValueError("Dataset contains duplicate customer IDs.")

    if effects["customer_id"].duplicated().any():
        raise ValueError("DML results contain duplicate customer IDs.")

    merged = df.merge(
        effects,
        on="customer_id",
        how="inner",
        validate="one_to_one",
    )

    if len(merged) != len(df) or len(merged) != len(effects):
        raise ValueError("Dataset and DML results do not match by customer.")

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
    dml_effect = merged["estimated_discount_effect"].to_numpy()

    report = pd.DataFrame({
        "customer_id": merged["customer_id"],
        "true_policy_effect": true_effect,
        "estimated_dml_effect": dml_effect,
        "absolute_error": np.abs(dml_effect - true_effect),
    })

    true_ate = float(np.mean(true_effect))
    estimated_ate = float(np.mean(dml_effect))
    bias = estimated_ate - true_ate
    mae = float(report["absolute_error"].mean())
    rmse = float(np.sqrt(np.mean((dml_effect - true_effect) ** 2)))

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(REPORT_FILE, index=False)

    print("\nDML validation against synthetic ground truth")
    print("---------------------------------------------")
    print(f"Customers evaluated: {len(report)}")
    print(f"True policy ATE:      {true_ate:.6f}")
    print(f"Estimated DML ATE:    {estimated_ate:.6f}")
    print(f"ATE estimation bias:  {bias:.6f}")
    print(f"Individual-effect MAE:{mae:.6f}")
    print(f"Individual-effect RMSE:{rmse:.6f}")
    print(f"\nDetailed report saved to: {REPORT_FILE}")


if __name__ == "__main__":
    main()
