
"""Evaluate revenue and simulated profit across discount levels.

Cost ratios are illustrative assumptions, not real business data.
"""

from pathlib import Path

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
    """Summarize revenue and simulated profit by discount rate."""

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
        "units_sold",
        "revenue",
    ]

    missing = [column for column in required_columns if column not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    if df.empty:
        raise ValueError("The prepared dataset is empty.")

    if df[required_columns].isnull().any().any():
        raise ValueError("Required columns contain missing values.")

    if (df["original_price"] < 0).any():
        raise ValueError("Original prices cannot be negative.")

    if (df["units_sold"] < 0).any():
        raise ValueError("Units sold cannot be negative.")

    if not df["discount_rate"].between(0, 1).all():
        raise ValueError("Discount rates must be between 0 and 1.")

    unknown_categories = set(df["product_category"]) - set(UNIT_COST_RATIOS)
    if unknown_categories:
        raise ValueError(
            f"Missing cost ratios for categories: {sorted(unknown_categories)}"
        )

    # Estimate the product cost per unit using an assumed category-specific
    # fraction of original price.
    df["assumed_unit_cost"] = (
        df["original_price"]
        * df["product_category"].map(UNIT_COST_RATIOS)
    )

    # Cost of goods is incurred only for units actually sold.
    df["estimated_cost_of_goods"] = (
        df["assumed_unit_cost"] * df["units_sold"]
    )

    # Simulated profit before operating expenses, marketing costs, taxes,
    # shipping, and other business expenses.
    df["simulated_profit"] = (
        df["revenue"] - df["estimated_cost_of_goods"]
    )

    # Each row represents a customer, including customers who did not buy.
    summary = (
        df.groupby("discount_rate")
        .agg(
            customers=("customer_id", "count"),
            purchase_rate=("units_sold", lambda values: (values > 0).mean()),
            total_revenue=("revenue", "sum"),
            mean_revenue_per_customer=("revenue", "mean"),
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
    print("=" * 65)
    print(summary.round(4).to_string(index=False))

    print("\nInterpretation notes:")
    print("- Cost ratios are illustrative assumptions, not real product costs.")
    print("- Simulated profit excludes operating and other business expenses.")
    print("- Results do not establish a real-world optimal discount.")
    print(f"\nSaved results to: {OUTPUT_FILE}")

    return summary


if __name__ == "__main__":
    evaluate_pricing_profit()
