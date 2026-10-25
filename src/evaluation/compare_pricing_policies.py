
"""Compare discount policies on the same synthetic customers."""

from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "data" / "prepared_pricing.csv"
OUTPUT_FILE = PROJECT_ROOT / "reports" / "pricing_policy_comparison.csv"

DISCOUNTS = [0.00, 0.05, 0.10, 0.15, 0.20]

UNIT_COST_RATIOS = {
    "Electronics": 0.60,
    "Clothing": 0.50,
    "Home": 0.55,
    "Beauty": 0.40,
}


def calculate_purchase_probability(df, discount_rate):
    """Recalculate purchase probability for a proposed discount."""
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


def compare_policies():
    """Evaluate each discount policy using the same customers."""
    df = pd.read_csv(DATA_FILE)

    required_columns = {
        "age",
        "income",
        "past_purchases",
        "product_category",
        "original_price",
    }
    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    if df.empty:
        raise ValueError("The prepared dataset is empty.")

    df["unit_cost_ratio"] = df["product_category"].map(UNIT_COST_RATIOS)

    if df["unit_cost_ratio"].isna().any():
        raise ValueError("Dataset contains an unknown product category.")

    if (df["original_price"] <= 0).any():
        raise ValueError("Original prices must be greater than zero.")

    results = []

    for discount in DISCOUNTS:
        probability = calculate_purchase_probability(df, discount)
        discounted_price = df["original_price"] * (1 - discount)
        unit_cost = df["original_price"] * df["unit_cost_ratio"]

        # Generator assumption: purchasers buy 1 unit with probability
        # 0.85 and 2 units with probability 0.15; expected units = 1.15.
        expected_units = probability * 1.15
        expected_revenue = discounted_price * expected_units
        expected_cost = unit_cost * expected_units
        expected_profit = expected_revenue - expected_cost

        results.append({
            "discount_rate": discount,
            "customers": len(df),
            "expected_purchase_rate": probability.mean(),
            "expected_revenue_per_customer": expected_revenue.mean(),
            "expected_profit_per_customer": expected_profit.mean(),
            "total_expected_revenue": expected_revenue.sum(),
            "total_expected_profit": expected_profit.sum(),
        })

    result_df = pd.DataFrame(results)
    result_df = result_df.sort_values(
        "expected_profit_per_customer", ascending=False
    ).reset_index(drop=True)

    result_df["expected_purchase_rate"] = (
        result_df["expected_purchase_rate"].round(4)
    )
    for column in [
        "expected_revenue_per_customer",
        "expected_profit_per_customer",
        "total_expected_revenue",
        "total_expected_profit",
    ]:
        result_df[column] = result_df[column].round(2)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    result_df.to_csv(OUTPUT_FILE, index=False)

    print("\nPricing Policy Comparison — Same 10,000 Customers")
    print("=" * 76)
    print(result_df.to_string(index=False))
    print("\nAssumptions:")
    print("- Every discount is evaluated on the same customer dataset.")
    print("- Expected units per purchase = 1.15.")
    print("- Product-cost ratios are illustrative assumptions.")
    print("- Profit excludes operating and other business expenses.")
    print("- Results are model-based estimates, not real-world proof.")
    print(f"\nSaved results to: {OUTPUT_FILE}")


if __name__ == "__main__":
    compare_policies()
