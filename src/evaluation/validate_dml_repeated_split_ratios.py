"""Validate LinearDML across repeated train/test split ratios."""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from econml.dml import LinearDML

from src.evaluation.compare_dml_estimators import (
    DATA_FILE,
    SEEDS,
    FEATURES,
    true_average_effect,
    make_preprocessor,
    make_first_stage_models,
    calculate_metrics,
    validate_dataset,
)


ROOT = Path(__file__).resolve().parents[2]

TEST_RATIOS = [0.30, 0.25, 0.20]

RESULTS_FILE = (
    ROOT / "reports" / "dml_repeated_split_ratios_results.csv"
)

SUMMARY_FILE = (
    ROOT / "reports" / "dml_repeated_split_ratios_summary.csv"
)


def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

    df = pd.read_csv(DATA_FILE)
    validate_dataset(df)

    run_rows = []

    total_runs = len(TEST_RATIOS) * len(SEEDS)
    run_number = 0

    for test_ratio in TEST_RATIOS:
        for seed in SEEDS:
            run_number += 1

            print(
                f"\nRun {run_number}/{total_runs}: "
                f"Split {1-test_ratio:.0%}/{test_ratio:.0%}, "
                f"seed {seed}"
            )

            train_df, test_df = train_test_split(
                df,
                test_size=test_ratio,
                random_state=seed,
                stratify=df["treatment"],
            )

            truth = true_average_effect(test_df)

            # Fit preprocessing on training customers only.
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

            estimates = np.asarray(
                estimator.effect(X_test)
            ).reshape(-1)

            if not np.isfinite(estimates).all():
                raise ValueError(
                    f"Non-finite effects for split {test_ratio}, "
                    f"seed {seed}."
                )

            metrics = calculate_metrics(truth, estimates)

            run_rows.append({
                "test_ratio": test_ratio,
                "train_ratio": 1 - test_ratio,
                "seed": seed,
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

    for test_ratio, group in results.groupby(
        "test_ratio", sort=False
    ):
        row = {
            "train_ratio": float(group["train_ratio"].iloc[0]),
            "test_ratio": float(test_ratio),
            "runs": len(group),
            "training_customers_mean": group[
                "training_customers"
            ].mean(),
            "holdout_customers_mean": group[
                "holdout_customers"
            ].mean(),
        }

        for metric in metric_columns:
            row[f"{metric}_mean"] = group[metric].mean()
            row[f"{metric}_std"] = group[metric].std(ddof=1)

        summary_rows.append(row)

    summary = pd.DataFrame(summary_rows)

    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)

    results.to_csv(RESULTS_FILE, index=False)
    summary.to_csv(SUMMARY_FILE, index=False)

    print("\nIndividual repeated-seed results:")
    print(results.to_string(index=False))

    print("\nSplit-ratio summary:")
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
