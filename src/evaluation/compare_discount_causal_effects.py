"""Compare causal effects of individual discount levels against 0% control."""

from pathlib import Path

import numpy as np
import pandas as pd

from src.models.train_dml import evaluate_dml_holdout


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "data" / "prepared_pricing.csv"
OUTPUT_FILE = PROJECT_ROOT / "reports" / "discount_causal_effect_comparison.csv"

DISCOUNT_LEVELS = [0.05, 0.10, 0.15, 0.20]


def calculate_purchase_probability(df, discount_rate):
    """Calculate the generator's known purchase probability at a discount."""

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


def prepare_discount_comparison_data(df, discount_rate):
    """Keep only one discount arm and the shared 0% control group."""

    if discount_rate not in DISCOUNT_LEVELS:
        raise ValueError(f"Unsupported discount level: {discount_rate}")

    comparison = df.loc[
        df["discount_rate"].isin([0.0, discount_rate])
    ].copy()

    comparison["treatment"] = (
        comparison["discount_rate"] == discount_rate
    ).astype(int)

    if set(comparison["treatment"].unique()) != {0, 1}:
        raise ValueError(
            f"Both control and {discount_rate:.0%} discount customers "
            "must be present."
        )

    return comparison


def evaluate_discount_level(df, discount_rate):
    """Estimate one discount's effect against 0% using holdout DML."""

    comparison = prepare_discount_comparison_data(df, discount_rate)

    holdout_effects = evaluate_dml_holdout(comparison)

    holdout_customers = comparison.merge(
        holdout_effects,
        on="customer_id",
        how="inner",
        validate="one_to_one",
    )

    if len(holdout_customers) != len(holdout_effects):
        raise ValueError("Holdout customer matching failed.")

    probability_control = calculate_purchase_probability(
        holdout_customers, 0.0
    )
    probability_discount = calculate_purchase_probability(
        holdout_customers, discount_rate
    )

    true_effects = probability_discount - probability_control
    estimated_effects = holdout_customers[
        "estimated_discount_effect"
    ].to_numpy()

    errors = estimated_effects - true_effects

    return {
        "discount_rate": discount_rate,
        "control_customers": int(
            (comparison["treatment"] == 0).sum()
        ),
        "discount_customers": int(
            (comparison["treatment"] == 1).sum()
        ),
        "holdout_customers": len(holdout_customers),
        "true_ate": float(np.mean(true_effects)),
        "estimated_ate": float(np.mean(estimated_effects)),
        "ate_bias": float(np.mean(errors)),
        "individual_effect_mae": float(np.mean(np.abs(errors))),
        "individual_effect_rmse": float(np.sqrt(np.mean(errors ** 2))),
    }


def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Prepared pricing data not found: {DATA_FILE}")

    df = pd.read_csv(DATA_FILE)

    required_columns = {
        "customer_id",
        "age",
        "income",
        "past_purchases",
        "product_category",
        "discount_rate",
        "purchase",
    }

    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    if df.empty:
        raise ValueError("Prepared pricing data is empty.")

    if df["customer_id"].duplicated().any():
        raise ValueError("Customer IDs must be unique.")

    results = []

    for discount_rate in DISCOUNT_LEVELS:
        print(f"\nEvaluating {discount_rate:.0%} discount against 0%...")
        results.append(evaluate_discount_level(df, discount_rate))

    report = pd.DataFrame(results)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(OUTPUT_FILE, index=False)

    print("\nDiscount-specific DML holdout comparison")
    print("----------------------------------------")
    print(report.to_string(index=False, float_format=lambda value: f"{value:.6f}"))
    print(f"\nReport saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()