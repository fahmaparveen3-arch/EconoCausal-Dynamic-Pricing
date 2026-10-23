
"""Generate reproducible synthetic retail pricing data for EconoCausal."""

from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_FILE = DATA_DIR / "synthetic_pricing.csv"

N_ROWS = 10_000
RANDOM_SEED = 42


def generate_pricing_data(n_rows=N_ROWS, random_seed=RANDOM_SEED):
    """Generate synthetic customer-level pricing and purchase outcomes."""
    rng = np.random.default_rng(random_seed)

    customer_id = np.arange(1, n_rows + 1)
    age = rng.integers(18, 71, size=n_rows)
    income = np.clip(
        rng.normal(45000, 18000, size=n_rows), 12000, 150000
    ).round(2)

    past_purchases = np.clip(rng.poisson(4, size=n_rows), 0, 25)

    product_category = rng.choice(
        ["Electronics", "Clothing", "Home", "Beauty"],
        size=n_rows,
        p=[0.25, 0.30, 0.25, 0.20],
    )

    original_price = np.select(
        [
            product_category == "Electronics",
            product_category == "Clothing",
            product_category == "Home",
            product_category == "Beauty",
        ],
        [
            rng.uniform(100, 1500, n_rows),
            rng.uniform(20, 250, n_rows),
            rng.uniform(30, 600, n_rows),
            rng.uniform(10, 150, n_rows),
        ],
    ).round(2)

    # Randomly assign customers to discount and control groups.
    treatment = rng.binomial(1, 0.5, size=n_rows)

    discount_rate = np.zeros(n_rows)
    treated = treatment == 1
    discount_rate[treated] = rng.choice(
        [0.05, 0.10, 0.15, 0.20],
        size=treated.sum(),
    )

    baseline_log_odds = (
        -2.0
        + 0.025 * (age - 40)
        + 0.000015 * (income - 45000)
        + 0.12 * past_purchases
        + 0.20 * (product_category == "Beauty")
        - 0.15 * (product_category == "Electronics")
    )

    discount_sensitivity = (
        3.0
        + 0.08 * past_purchases
        + 0.00001 * (income - 45000)
    )

    log_odds = baseline_log_odds + discount_sensitivity * discount_rate
    purchase_probability = 1 / (1 + np.exp(-log_odds))
    purchase = rng.binomial(1, purchase_probability)

    units_sold = np.where(
        purchase == 1,
        rng.choice([1, 2], size=n_rows, p=[0.85, 0.15]),
        0,
    )

    discounted_price = original_price * (1 - discount_rate)
    revenue = (discounted_price * units_sold).round(2)
    discount_cost = (original_price * discount_rate * units_sold).round(2)

    return pd.DataFrame({
        "customer_id": customer_id,
        "age": age,
        "income": income,
        "past_purchases": past_purchases,
        "product_category": product_category,
        "original_price": original_price,
        "discount_rate": discount_rate,
        "treatment": treatment,
        "purchase": purchase,
        "units_sold": units_sold,
        "discounted_price": discounted_price.round(2),
        "revenue": revenue,
        "discount_cost": discount_cost,
        "purchase_probability": purchase_probability.round(6),
    })


if __name__ == "__main__":
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    df = generate_pricing_data()
    df.to_csv(OUTPUT_FILE, index=False)

    print("Synthetic pricing dataset generated successfully!")
    print(f"Saved to: {OUTPUT_FILE}")
    print(f"Dataset shape: {df.shape}")
    print(f"Missing values: {df.isna().sum().sum()}")
    print(f"Unique customers: {df['customer_id'].nunique()}")

    print("\nTreatment group counts:")
    print(df["treatment"].value_counts().sort_index())

    print("\nPurchase rates by treatment:")
    print(df.groupby("treatment")["purchase"].mean())

    print("\nFirst five rows:")
    print(df.head())
