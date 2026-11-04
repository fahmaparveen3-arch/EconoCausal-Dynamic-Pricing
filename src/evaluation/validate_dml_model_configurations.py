"""Test LinearDML sensitivity to Random Forest configurations."""

from pathlib import Path

import numpy as np
import pandas as pd
from econml.dml import LinearDML
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split

from src.evaluation.compare_dml_estimators import (
    DATA_FILE,
    FEATURES,
    SEEDS,
    calculate_metrics,
    make_preprocessor,
    true_average_effect,
    validate_dataset,
)

ROOT = Path(__file__).resolve().parents[2]

RESULTS_FILE = ROOT / "reports" / "dml_model_configuration_results.csv"
SUMMARY_FILE = ROOT / "reports" / "dml_model_configuration_summary.csv"

TEST_SIZE = 0.20

CONFIGURATIONS = {
    "Baseline_100_Trees_Leaf_20": {
        "n_estimators": 100,
        "min_samples_leaf": 20,
    },
    "Config_A_100_Trees_Leaf_10": {
        "n_estimators": 100,
        "min_samples_leaf": 10,
    },
    "Config_B_200_Trees_Leaf_20": {
        "n_estimators": 200,
        "min_samples_leaf": 20,
    },
}


def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

    df = pd.read_csv(DATA_FILE)
    validate_dataset(df)

    run_rows = []

    for config_name, config in CONFIGURATIONS.items():
        print(f"\nConfiguration: {config_name}")
        print(f"Settings: {config}")

        for seed in SEEDS:
            print(f"  Evaluating seed {seed}...")

            train_df, test_df = train_test_split(
                df,
                test_size=TEST_SIZE,
                random_state=seed,
                stratify=df["treatment"],
            )

            truth = true_average_effect(test_df)

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

            model_y = RandomForestRegressor(
                n_estimators=config["n_estimators"],
                min_samples_leaf=config["min_samples_leaf"],
                random_state=seed,
                n_jobs=-1,
            )

            model_t = RandomForestClassifier(
                n_estimators=config["n_estimators"],
                min_samples_leaf=config["min_samples_leaf"],
                random_state=seed,
                n_jobs=-1,
            )

            estimator = LinearDML(
                model_y=model_y,
                model_t=model_t,
                discrete_treatment=True,
                fit_cate_intercept=True,
                cv=3,
                random_state=seed,
            )

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
                    f"Non-finite effects for {config_name}, seed {seed}."
                )

            metrics = calculate_metrics(truth, estimates)

            run_rows.append({
                "configuration": config_name,
                "n_estimators": config["n_estimators"],
                "min_samples_leaf": config["min_samples_leaf"],
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

    for config_name, group in results.groupby(
        "configuration", sort=False
    ):
        row = {
            "configuration": config_name,
            "runs": len(group),
            "n_estimators": int(group["n_estimators"].iloc[0]),
            "min_samples_leaf": int(
                group["min_samples_leaf"].iloc[0]
            ),
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

    print("\nIndividual experiment results:")
    print(results.to_string(
        index=False,
        float_format=lambda value: f"{value:.6f}",
    ))

    print("\nConfiguration summary:")
    print(summary.to_string(
        index=False,
        float_format=lambda value: f"{value:.6f}",
    ))

    print(f"\nIndividual results saved to: {RESULTS_FILE}")
    print(f"Summary saved to: {SUMMARY_FILE}")


if __name__ == "__main__":
    main()
