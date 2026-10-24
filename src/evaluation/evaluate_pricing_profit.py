
"""Evaluate revenue and simulated profit across discount levels.

Cost ratios are illustrative assumptions, not real business data.
"""

from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "data" / "prepared_pricing.csv"
OUTPUT_FILE = PROJECT_ROOT / "reports" / "pricing_profit_evaluation.csv"

# Illustrative product cost as a fraction of original price.
# These assumptions are for demonstration only.
UNIT_COST_RATIOS = {
    "Electronics": 0.60,
    "Clothing": 0.50,
    "Home": 0.55,
    "Beauty": 0.40,
}


def evaluate_pricing_profit():
    """Validate pricing calculations and summarize simulated profit."""

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Prepared dataset not found: {DATA_FILE}. "
            "Run src/data_processing/prepare_pricing_data.py first."
        )

    df = pd.read_csv(DATA_FILE)

    required_columns = [
        "customer_id",
        "product_category",
        "original_price",
        "discount_rate",
        "discounted_price",
        "discount_cost",
        "units_sold",
        "revenue",
    ]

    missing = [
        column for column in required_columns if column not in df.columns
    ]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    if df.empty:
        raise ValueError("The prepared dataset is empty.")

    if df[required_columns].isnull().any().any():
        raise ValueError("Required columns contain missing values.")

    numeric_columns = [
        "original_price",
        "discount_rate",
        "discounted_price",
        "discount_cost",
        "units_sold",
        "revenue",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="raise")

    if not np.isfinite(df[numeric_columns].to_numpy(dtype=float)).all():
        raise ValueError("Pricing data contains non-finite numeric values.")

    if (df["original_price"] < 0).any():
        raise ValueError("Original prices cannot be negative.")

    if (df["units_sold"] < 0).any():
        raise ValueError("Units sold cannot be negative.")

    if not df["discount_rate"].between(0, 1).all():
        raise ValueError("Discount rates must be between 0 and 1.")

    if df["customer_id"].duplicated().any():
        raise ValueError("Customer IDs must be unique.")

    if (df["discounted_price"] < 0).any():
        raise ValueError("Discounted prices cannot be negative.")

    if (df["revenue"] < 0).any() or (df["discount_cost"] < 0).any():
        raise ValueError("Revenue and discount cost cannot be negative.")

    # Validate prices and revenue against the pricing formulas.
    expected_price = (
        df["original_price"] * (1 - df["discount_rate"])
    ).round(2)

    expected_revenue = (
        expected_price * df["units_sold"]
    ).round(2)

    expected_discount_cost = (
        df["original_price"]
        * df["discount_rate"]
        * df["units_sold"]
    ).round(2)

    if not np.allclose(
        df["discounted_price"], expected_price, atol=0.011, rtol=0
    ):
        raise ValueError(
            "Discounted prices do not match the expected pricing formula."
        )

    if not np.allclose(
        df["revenue"], expected_revenue, atol=0.011, rtol=0
    ):
        raise ValueError(
            "Revenue does not match discounted price multiplied by units sold."
        )

    if not np.allclose(
        df["discount_cost"], expected_discount_cost, atol=0.011, rtol=0
    ):
        raise ValueError(
            "Discount costs do not match the expected discount formula."
        )

    unknown_categories = set(df["product_category"]) - set(UNIT_COST_RATIOS)
    if unknown_categories:
        raise ValueError(
            f"Missing cost ratios for categories: {sorted(unknown_categories)}"
        )

    # Estimate product cost using illustrative category-specific ratios.
    df["assumed_unit_cost"] = (
        df["original_price"]
        * df["product_category"].map(UNIT_COST_RATIOS)
    )

    # Product costs apply only to units actually sold.
    df["estimated_cost_of_goods"] = (
        df["assumed_unit_cost"] * df["units_sold"]
    )

    # Revenue already includes the discount. Do not subtract discount_cost
    # again. This profit estimate excludes other business expenses.
    df["simulated_profit"] = (
        df["revenue"] - df["estimated_cost_of_goods"]
    )

    # Each row represents one customer, including non-buyers.
    summary = (
        df.groupby("discount_rate")
        .agg(
            customers=("customer_id", "count"),
            purchase_rate=("units_sold", lambda values: (values > 0).mean()),
            total_revenue=("revenue", "sum"),
            mean_revenue_per_customer=("revenue", "mean"),
            total_discount_cost=("discount_cost", "sum"),
            total_estimated_cost=("estimated_cost_of_goods", "sum"),
            total_simulated_profit=("simulated_profit", "sum"),
            mean_simulated_profit_per_customer=("simulated_profit", "mean"),
        )
        .reset_index()
        .sort_values("discount_rate")
    )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(OUTPUT_FILE, index=False)

    print("\nPricing Evaluation — Synthetic Data")
    print("=" * 75)
    print(summary.round(4).to_string(index=False))

    print("\nValidation successful:")
    print("- Discounted prices, revenue, and discount costs match their formulas.")
    print("- Discount cost is not subtracted twice from revenue.")
    print("- Product-cost ratios are illustrative assumptions.")
    print("- Simulated profit excludes operating and other business expenses.")
    print("- Results do not establish a real-world optimal discount.")
    print(f"\nSaved results to: {OUTPUT_FILE}")

    return summary


if __name__ == "__main__":
    evaluate_pricing_profit()
