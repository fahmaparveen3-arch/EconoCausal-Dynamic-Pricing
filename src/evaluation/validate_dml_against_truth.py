
"""Repeated-seed holdout validation against synthetic treatment truth."""

from pathlib import Path

import numpy as np
import pandas as pd

from src.models.train_dml import evaluate_dml_holdout


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "data" / "prepared_pricing.csv"

RESULTS_FILE = (
    PROJECT_ROOT / "reports" / "dml_truth_repeated_seed_results.csv"
)

SUMMARY_FILE = (
    PROJECT_ROOT / "reports" / "dml_truth_repeated_seed_summary.csv"
)

SEEDS = [42, 7, 21, 35, 99]
DISCOUNT_LEVELS = [0.05, 0.10, 0.15, 0.20]


def calculate_discount_weights(df):
    """Calculate actual discount proportions among treated customers."""

    treated = df.loc[df["treatment"] == 1, "discount_rate"]

    if treated.empty:
        raise ValueError("No treated customers found.")

    counts = treated.value_counts()

    missing_levels = set(DISCOUNT_LEVELS) - set(counts.index)

    if missing_levels:
        raise ValueError(
            f"Missing discount levels: {sorted(missing_levels)}"
        )

    weights = (
        counts.reindex(DISCOUNT_LEVELS).to_numpy(dtype=float)
        / len(treated)
    )

    print("\nActual discount proportions:")
    for discount, weight in zip(DISCOUNT_LEVELS, weights):
        print(f"{discount:.0%} discount: {weight:.4%}")

    return weights


def calculate_true_effects(df, discount_weights):
    """Calculate true effects using the actual discount mixture."""

    age = df["age"].to_numpy(dtype=float)
    income = df["income"].to_numpy(dtype=float)
    past_purchases = df["past_purchases"].to_numpy(dtype=float)
    category = df["product_category"].to_numpy()

    baseline = (
        -2
        + 0.025 * (age - 40)
        + 0.000015 * (income - 45000)
        + 0.12 * past_purchases
        + 0.20 * (category == "Beauty")
        - 0.15 * (category == "Electronics")
    )

    sensitivity = (
        3
        + 0.08 * past_purchases
        + 0.00001 * (income - 45000)
    )

    def sigmoid(value):
        return 1 / (1 + np.exp(-value))

    effects = np.column_stack([
        sigmoid(baseline + sensitivity * discount)
        - sigmoid(baseline)
        for discount in DISCOUNT_LEVELS
    ])

    return np.average(
        effects,
        axis=1,
        weights=discount_weights,
    )


def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Prepared pricing dataset not found: {DATA_FILE}"
        )

    df = pd.read_csv(DATA_FILE)

    if df.empty:
        raise ValueError("Prepared pricing dataset is empty.")

    required_columns = {
        "customer_id",
        "age",
        "income",
        "past_purchases",
        "product_category",
        "discount_rate",
        "treatment",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    discount_weights = calculate_discount_weights(df)

    run_rows = []

    for seed in SEEDS:
        print(f"\nEvaluating holdout validation with seed {seed}...")

        estimated = evaluate_dml_holdout(
            df,
            test_size=0.25,
            random_state=seed,
        )

        holdout = df.merge(
            estimated,
            on="customer_id",
            how="inner",
            validate="one_to_one",
        )

        if len(holdout) != len(estimated):
            raise ValueError(
                f"Customer matching failed for seed {seed}."
            )

        true_effects = calculate_true_effects(
            holdout,
            discount_weights,
        )

        predicted_effects = (
            holdout["estimated_discount_effect"].to_numpy()
        )

        errors = predicted_effects - true_effects

        correlation = (
            float(np.corrcoef(true_effects, predicted_effects)[0, 1])
            if np.std(true_effects) > 0
            and np.std(predicted_effects) > 0
            else np.nan
        )

        true_ate = float(np.mean(true_effects))
        estimated_ate = float(np.mean(predicted_effects))

        run_rows.append({
            "seed": seed,
            "holdout_customers": len(holdout),
            "true_ate": true_ate,
            "estimated_ate": estimated_ate,
            "ate_bias": estimated_ate - true_ate,
            "absolute_ate_bias": abs(estimated_ate - true_ate),
            "mae": float(np.mean(np.abs(errors))),
            "rmse": float(np.sqrt(np.mean(errors ** 2))),
            "effect_correlation": correlation,
        })

    results = pd.DataFrame(run_rows)

    metric_columns = [
        "true_ate",
        "estimated_ate",
        "ate_bias",
        "absolute_ate_bias",
        "mae",
        "rmse",
        "effect_correlation",
    ]

    summary_rows = []

    for metric in metric_columns:
        summary_rows.append({
            "metric": metric,
            "mean": results[metric].mean(),
            "std": results[metric].std(ddof=1),
            "minimum": results[metric].min(),
            "maximum": results[metric].max(),
        })

    summary = pd.DataFrame(summary_rows)

    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)

    results.to_csv(RESULTS_FILE, index=False)
    summary.to_csv(SUMMARY_FILE, index=False)

    print("\nIndividual repeated-seed results:")
    print(results.to_string(index=False))

    print("\nRepeated-seed summary:")
    print(
        summary.to_string(
            index=False,
            float_format=lambda value: f"{value:.6f}",
        )
    )

    print(f"\nIndividual results saved to: {RESULTS_FILE}")
    print(f"Summary saved to: {SUMMARY_FILE}")


if __name__ == "__main__":
    main()
