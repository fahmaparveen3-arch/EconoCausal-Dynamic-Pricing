"""Compare Difference-in-Means and DML estimators across five holdout splits."""

from pathlib import Path

import numpy as np
import pandas as pd
from econml.dml import LinearDML, NonParamDML
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import (
    GradientBoostingRegressor,
    RandomForestClassifier,
    RandomForestRegressor,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder


ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = ROOT / "data" / "prepared_pricing.csv"

REPORT_FILE = (
    ROOT / "reports" / "dml_estimator_repeated_seed_summary.csv"
)

RUN_RESULTS_FILE = (
    ROOT / "reports" / "dml_estimator_repeated_seed_results.csv"
)

FEATURES = ["age", "income", "past_purchases", "product_category"]
DISCOUNTS = [0.05, 0.10, 0.15, 0.20]
SEEDS = [42, 7, 21, 35, 99]


def true_purchase_probability(df, discount):
    """Recreate the probability formula used by the synthetic generator."""
    category = df["product_category"]

    baseline_log_odds = (
        -2
        + 0.025 * (df["age"] - 40)
        + 0.000015 * (df["income"] - 45000)
        + 0.12 * df["past_purchases"]
        + 0.20 * (category == "Beauty").astype(float)
        - 0.15 * (category == "Electronics").astype(float)
    )

    discount_sensitivity = (
        3.0
        + 0.08 * df["past_purchases"]
        + 0.00001 * (df["income"] - 45000)
    )

    log_odds = baseline_log_odds + discount_sensitivity * discount

    return 1 / (1 + np.exp(-log_odds))


def true_average_effect(df):
    """Calculate true effects using actual treated discount proportions."""
    treated_rates = df.loc[df["treatment"] == 1, "discount_rate"]

    if treated_rates.empty:
        raise ValueError("No treated customers found.")

    counts = treated_rates.value_counts()
    missing_levels = set(DISCOUNTS) - set(counts.index)

    if missing_levels:
        raise ValueError(
            f"Missing discount levels: {sorted(missing_levels)}"
        )

    discount_weights = (
        counts.reindex(DISCOUNTS).to_numpy(dtype=float)
        / len(treated_rates)
    )

    control_probability = true_purchase_probability(df, 0.0)

    effects = [
        true_purchase_probability(df, discount) - control_probability
        for discount in DISCOUNTS
    ]

    return np.average(
        np.column_stack(effects),
        axis=1,
        weights=discount_weights,
    )


def estimate_difference_in_means(train_df):
    """Estimate the average treatment effect using training data only."""
    if train_df.empty:
        raise ValueError("Training data cannot be empty.")

    required = ["treatment", "purchase"]
    missing = [column for column in required if column not in train_df.columns]

    if missing:
        raise ValueError(
            f"Training data is missing required columns: {missing}"
        )

    if train_df[required].isnull().any().any():
        raise ValueError(
            "Treatment and purchase cannot contain missing values."
        )

    if set(train_df["treatment"].unique()) != {0, 1}:
        raise ValueError(
            "Both treatment and control groups are required."
        )

    if not set(train_df["purchase"].unique()).issubset({0, 1}):
        raise ValueError("Purchase must contain only 0 and 1.")

    treatment_groups = train_df.groupby("treatment")["purchase"].mean()

    return float(treatment_groups.loc[1] - treatment_groups.loc[0])


def calculate_baseline_metrics(train_df, truth):
    """
    Evaluate the Difference-in-Means ATE against holdout ground truth.

    Difference-in-Means estimates an average effect, not individual
    customer effects. Therefore individual-effect metrics are not calculated.
    """
    truth = np.asarray(truth, dtype=float)

    if truth.size == 0 or not np.isfinite(truth).all():
        raise ValueError("Holdout ground truth must contain finite values.")

    estimated_ate = estimate_difference_in_means(train_df)
    true_ate = float(np.mean(truth))
    ate_bias = estimated_ate - true_ate

    return {
        "true_ate": true_ate,
        "estimated_ate": estimated_ate,
        "ate_bias": ate_bias,
        "absolute_ate_bias": abs(ate_bias),
        "mae": np.nan,
        "rmse": np.nan,
        "effect_correlation": np.nan,
    }


def make_preprocessor():
    """Create the feature preprocessing pipeline."""
    return ColumnTransformer(
        transformers=[
            (
                "category",
                OneHotEncoder(
                    drop="first",
                    handle_unknown="ignore",
                    sparse_output=False,
                ),
                ["product_category"],
            )
        ],
        remainder="passthrough",
    )


def make_first_stage_models(seed):
    """Create fresh first-stage models for a particular run."""
    return {
        "model_y": RandomForestRegressor(
            n_estimators=100,
            min_samples_leaf=20,
            random_state=seed,
            n_jobs=-1,
        ),
        "model_t": RandomForestClassifier(
            n_estimators=100,
            min_samples_leaf=20,
            random_state=seed,
            n_jobs=-1,
        ),
    }


def calculate_metrics(truth, estimates):
    """Calculate DML holdout metrics."""
    truth = np.asarray(truth, dtype=float)
    estimates = np.asarray(estimates, dtype=float)

    if len(truth) != len(estimates):
        raise ValueError("Truth and estimates must have equal lengths.")

    if len(truth) == 0:
        raise ValueError("Truth and estimates cannot be empty.")

    if not np.isfinite(truth).all() or not np.isfinite(estimates).all():
        raise ValueError("Truth and estimates must contain finite values.")

    errors = estimates - truth

    if np.std(truth) == 0 or np.std(estimates) == 0:
        correlation = np.nan
    else:
        correlation = float(np.corrcoef(truth, estimates)[0, 1])

    ate_bias = float(np.mean(errors))

    return {
        "true_ate": float(np.mean(truth)),
        "estimated_ate": float(np.mean(estimates)),
        "ate_bias": ate_bias,
        "absolute_ate_bias": abs(ate_bias),
        "mae": float(np.mean(np.abs(errors))),
        "rmse": float(np.sqrt(np.mean(errors**2))),
        "effect_correlation": correlation,
    }


def validate_dataset(df):
    """Validate the prepared pricing dataset."""
    required = FEATURES + ["customer_id", "treatment", "purchase"]

    missing = [column for column in required if column not in df.columns]

    if missing:
        raise ValueError(
            f"Dataset is missing required columns: {missing}"
        )

    if df.empty or df[required].isnull().any().any():
        raise ValueError(
            "Dataset is empty or required columns contain missing values."
        )

    if df["customer_id"].duplicated().any():
        raise ValueError("Customer IDs must be unique.")

    if set(df["treatment"].unique()) != {0, 1}:
        raise ValueError("Treatment must contain both 0 and 1.")

    if set(df["purchase"].unique()) != {0, 1}:
        raise ValueError("Purchase must contain both 0 and 1.")


def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

    df = pd.read_csv(DATA_FILE)

    validate_dataset(df)

    run_rows = []

    for seed in SEEDS:
        print(f"\nEvaluating seed {seed}...")

        train_df, test_df = train_test_split(
            df,
            test_size=0.25,
            random_state=seed,
            stratify=df["treatment"],
        )

        # Calculate the synthetic reference effects for holdout customers.
        truth = true_average_effect(test_df)

        # ---------------------------------------------------------
        # 1. Difference-in-Means baseline
        # ---------------------------------------------------------
        print("  Evaluating Difference-in-Means baseline...")

        baseline_metrics = calculate_baseline_metrics(
            train_df,
            truth,
        )

        run_rows.append(
            {
                "seed": seed,
                "estimator": "Difference-in-Means",
                "holdout_customers": len(test_df),
                **baseline_metrics,
            }
        )

        # ---------------------------------------------------------
        # 2. Prepare features for DML estimators
        # ---------------------------------------------------------
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

        # ---------------------------------------------------------
        # 3. DML estimators
        # ---------------------------------------------------------
        estimators = {
            "LinearDML": LinearDML(
                **make_first_stage_models(seed),
                discrete_treatment=True,
                fit_cate_intercept=True,
                cv=3,
                random_state=seed,
            ),
            "NonParamDML_GradientBoosting": NonParamDML(
                **make_first_stage_models(seed),
                model_final=GradientBoostingRegressor(
                    n_estimators=100,
                    learning_rate=0.05,
                    max_depth=2,
                    min_samples_leaf=20,
                    random_state=seed,
                ),
                discrete_treatment=True,
                cv=3,
                random_state=seed,
            ),
        }

        for name, estimator in estimators.items():
            print(f"  Fitting {name}...")

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
                    f"{name} produced non-finite effects for seed {seed}."
                )

            metrics = calculate_metrics(truth, estimates)

            run_rows.append(
                {
                    "seed": seed,
                    "estimator": name,
                    "holdout_customers": len(test_df),
                    **metrics,
                }
            )

    # ---------------------------------------------------------
    # 4. Create detailed results
    # ---------------------------------------------------------
    run_results = pd.DataFrame(run_rows)

    metric_columns = [
        "true_ate",
        "estimated_ate",
        "ate_bias",
        "absolute_ate_bias",
        "mae",
        "rmse",
        "effect_correlation",
    ]

    # ---------------------------------------------------------
    # 5. Create repeated-seed summary
    # ---------------------------------------------------------
    summary_rows = []

    for name, group in run_results.groupby("estimator", sort=False):
        row = {
            "estimator": name,
            "runs": len(group),
            "holdout_customers_per_run": int(
                group["holdout_customers"].iloc[0]
            ),
        }

        for metric in metric_columns:
            row[f"{metric}_mean"] = group[metric].mean()
            row[f"{metric}_std"] = group[metric].std(ddof=1)

        summary_rows.append(row)

    summary = pd.DataFrame(summary_rows)

    # ---------------------------------------------------------
    # 6. Save reports
    # ---------------------------------------------------------
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    run_results.to_csv(RUN_RESULTS_FILE, index=False)
    summary.to_csv(REPORT_FILE, index=False)

    print("\nIndividual seed-level results:")
    print(run_results.to_string(index=False))

    print("\nRepeated-seed estimator summary:")
    print(
        summary.to_string(
            index=False,
            float_format=lambda value: f"{value:.6f}",
        )
    )

    print(f"\nSaved individual results to: {RUN_RESULTS_FILE}")
    print(f"Saved summary report to: {REPORT_FILE}")


if __name__ == "__main__":
    main()