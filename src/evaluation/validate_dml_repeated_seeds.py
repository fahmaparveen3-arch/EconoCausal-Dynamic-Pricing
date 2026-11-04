"""Validate LinearDML stability across five 80/20 holdout splits."""

from pathlib import Path

import numpy as np
import pandas as pd
from econml.dml import LinearDML
from sklearn.model_selection import train_test_split

from src.evaluation.compare_dml_estimators import (
    DATA_FILE,
    SEEDS,
    calculate_baseline_metrics,
    calculate_metrics,
    make_first_stage_models,
    make_preprocessor,
    true_average_effect,
    validate_dataset,
    FEATURES,
)

ROOT = Path(__file__).resolve().parents[2]
TEST_SIZE = 0.20

RESULTS_FILE = ROOT / "reports" / "dml_repeated_seed_80_20_results.csv"
SUMMARY_FILE = ROOT / "reports" / "dml_repeated_seed_80_20_summary.csv"


def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

    df = pd.read_csv(DATA_FILE)
    validate_dataset(df)

    run_rows = []

    for seed in SEEDS:
        print(f"\nEvaluating seed {seed} with 80/20 split...")

        train_df, test_df = train_test_split(
            df,
            test_size=TEST_SIZE,
            random_state=seed,
            stratify=df["treatment"],
        )

        truth = true_average_effect(test_df)

        baseline_metrics = calculate_baseline_metrics(train_df, truth)

        run_rows.append({
            "seed": seed,
            "estimator": "Difference-in-Means",
            "training_customers": len(train_df),
            "holdout_customers": len(test_df),
            **baseline_metrics,
        })

        preprocessor = make_preprocessor()

        X_train = np.asarray(
            preprocessor.fit_transform(train_df[FEATURES]),
            dtype=float,
        )
        X_test = np.asarray(
            preprocessor.transform(test_df[FEATURES]),
            dtype=float,
        )

        y_train = train_df["purchase"].to_numpy(dtype=float)
        t_train = train_df["treatment"].to_numpy(dtype=int)

        estimator = LinearDML(
            **make_first_stage_models(seed),
            discrete_treatment=True,
            fit_cate_intercept=True,
            cv=3,
            random_state=seed,
        )

        print("  Fitting LinearDML...")

        estimator.fit(
            y_train,
            t_train,
            X=X_train,
            inference=None,
        )

        estimates = np.asarray(estimator.effect(X_test)).reshape(-1)

        if not np.isfinite(estimates).all():
            raise ValueError(
                f"LinearDML produced non-finite effects for seed {seed}."
            )

        metrics = calculate_metrics(truth, estimates)

        run_rows.append({
            "seed": seed,
            "estimator": "LinearDML",
            "training_customers": len(train_df),
            "holdout_customers": len(test_df),
            **metrics,
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

    for name, group in results.groupby("estimator", sort=False):
        row = {
            "estimator": name,
            "runs": len(group),
            "training_customers_per_run": int(
                group["training_customers"].iloc[0]
            ),
            "holdout_customers_per_run": int(
                group["holdout_customers"].iloc[0]
            ),
        }

        for metric in metric_columns:
            row[f"{metric}_mean"] = group[metric].mean()
            row[f"{metric}_std"] = group[metric].std(ddof=1)

        summary_rows.append(row)

    summary = pd.DataFrame(summary_rows)

    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(RESULTS_FILE, index=False)
    summary.to_csv(SUMMARY_FILE, index=False)

    print("\nIndividual seed-level results:")
    print(results.to_string(index=False))

    print("\nRepeated-seed summary:")
    print(summary.to_string(
        index=False,
        float_format=lambda value: f"{value:.6f}",
    ))

    print(f"\nIndividual results saved to: {RESULTS_FILE}")
    print(f"Summary saved to: {SUMMARY_FILE}")


if __name__ == "__main__":
    main()
