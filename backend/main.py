
from pathlib import Path
from math import erfc, sqrt

import numpy as np
import pandas as pd

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
REPORTS_DIR = ROOT_DIR / "reports"


# --------------------------------------------------
# APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="EconoCausal Dynamic Pricing API",
    description="Python backend for the EconoCausal dashboard",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# DATA HELPERS
# --------------------------------------------------

def load_csv(directory: Path, filename: str) -> pd.DataFrame:
    path = directory / filename

    if not path.exists():
        raise HTTPException(
            status_code=503,
            detail=f"Required data file not found: {filename}",
        )

    try:
        return pd.read_csv(path)

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Could not read {filename}: {str(exc)}",
        )


def validate_dataframe(
    df: pd.DataFrame,
    filename: str,
    required_columns: set,
) -> None:

    if df.empty:
        raise HTTPException(
            status_code=500,
            detail=f"Required data file is empty: {filename}",
        )

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise HTTPException(
            status_code=500,
            detail=(
                f"{filename} is missing required columns: "
                f"{', '.join(sorted(missing_columns))}"
            ),
        )


def clean_records(df: pd.DataFrame) -> list:
    records = []

    for record in df.to_dict(orient="records"):
        cleaned = {}

        for key, value in record.items():

            if pd.isna(value):
                cleaned[key] = None

            elif isinstance(value, np.generic):
                cleaned[key] = value.item()

            else:
                cleaned[key] = value

        records.append(cleaned)

    return records


def normalize_segment(value: str) -> str:
    return "".join(
        character
        for character in str(value).lower()
        if character.isalnum()
    )


# --------------------------------------------------
# CAUSAL ANALYSIS
# --------------------------------------------------

def calculate_hillstrom_effect(
    df: pd.DataFrame,
    treatment_segment: str,
    control_segment: str = "noemail",
) -> dict:

    segments = df["segment"].map(normalize_segment)

    treatment = df.loc[
        segments == treatment_segment,
        "conversion",
    ].astype(float)

    control = df.loc[
        segments == control_segment,
        "conversion",
    ].astype(float)

    if treatment.empty or control.empty:
        raise ValueError(
            f"Missing observations for {treatment_segment}"
        )

    p_treatment = float(treatment.mean())
    p_control = float(control.mean())

    effect = p_treatment - p_control

    standard_error = sqrt(
        p_treatment * (1 - p_treatment) / len(treatment)
        + p_control * (1 - p_control) / len(control)
    )

    z_score = effect / standard_error

    lower = effect - 1.96 * standard_error
    upper = effect + 1.96 * standard_error

    p_value = erfc(abs(z_score) / sqrt(2))

    return {
        "effect": round(effect * 100, 6),
        "lower": round(lower * 100, 6),
        "upper": round(upper * 100, 6),
        "p_value": p_value,
        "z_score": z_score,
        "treatment_customers": len(treatment),
        "control_customers": len(control),
        "treatment_conversion_rate": p_treatment * 100,
        "control_conversion_rate": p_control * 100,
    }


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "service": "EconoCausal Dynamic Pricing API",
        "version": "1.0.0",
    }


# --------------------------------------------------
# PRICING ANALYTICS
# --------------------------------------------------

def get_pricing_data():

    df = load_csv(
        REPORTS_DIR,
        "pricing_policy_comparison.csv",
    )

    validate_dataframe(
        df,
        "pricing_policy_comparison.csv",
        {
            "discount_rate",
            "customers",
            "expected_purchase_rate",
            "expected_revenue_per_customer",
            "expected_profit_per_customer",
            "total_expected_revenue",
            "total_expected_profit",
        },
    )

    df = df.sort_values("discount_rate")

    policies = []

    for row in clean_records(df):

        policies.append({
            "discount": f"{row['discount_rate'] * 100:g}%",
            "discount_rate": row["discount_rate"],
            "customers": row["customers"],
            "purchase_rate": row["expected_purchase_rate"] * 100,
            "revenue": row["expected_revenue_per_customer"],
            "profit": row["expected_profit_per_customer"],
            "total_revenue": row["total_expected_revenue"],
            "total_profit": row["total_expected_profit"],
        })

    best_policy = max(
        policies,
        key=lambda item: item["profit"],
    )

    causal_df = load_csv(
        REPORTS_DIR,
        "discount_causal_effect_comparison.csv",
    )

    validate_dataframe(
        causal_df,
        "discount_causal_effect_comparison.csv",
        {
            "discount_rate",
            "true_ate",
            "estimated_ate",
            "ate_bias",
            "individual_effect_mae",
            "individual_effect_rmse",
        },
    )

    pricing_effects = []

    for row in clean_records(
        causal_df.sort_values("discount_rate")
    ):

        pricing_effects.append({
            "discount": f"{row['discount_rate'] * 100:g}%",
            "true_ate": row["true_ate"] * 100,
            "estimated_ate": row["estimated_ate"] * 100,
            "bias": row["ate_bias"] * 100,
            "mae": row["individual_effect_mae"],
            "rmse": row["individual_effect_rmse"],
        })

    return {
        "dataset": "Synthetic pricing dataset",
        "customers": policies[0]["customers"],
        "policies": policies,
        "best_policy": best_policy,
        "causal_effects": pricing_effects,
        "disclaimer": (
            "Results are based on synthetic data and model "
            "assumptions. They do not establish a real-world "
            "optimal pricing strategy."
        ),
    }


@app.get("/api/pricing")
def pricing():
    return get_pricing_data()


# --------------------------------------------------
# HILLSTROM CAUSAL ANALYSIS
# --------------------------------------------------

def get_causal_data():

    df = load_csv(
        DATA_DIR,
        "hillstrom.csv",
    )

    validate_dataframe(
        df,
        "hillstrom.csv",
        {"segment", "conversion"},
    )

    try:
        men = calculate_hillstrom_effect(
            df,
            "mensemail",
        )

        women = calculate_hillstrom_effect(
            df,
            "womensemail",
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Hillstrom analysis failed: {str(exc)}",
        )

    segment_counts = (
        df["segment"].astype(str).str.lower()
        .str.replace(r"[^a-z]", "", regex=True)
        .value_counts()
    )

    return {
        "dataset": "Hillstrom randomized email experiment",
        "segment_counts": [
            {
                "name": "Men's Email",
                "value": int(segment_counts.get("mensemail", 0)),
            },
            {
                "name": "Women's Email",
                "value": int(segment_counts.get("womensemail", 0)),
            },
            {
                "name": "No Email",
                "value": int(segment_counts.get("noemail", 0)),
            },
        ],
        "customers": len(df),
        "control_group": "No Email",
        "effects": [
            {
                "segment": "Men's Email",
                **men,
            },
            {
                "segment": "Women's Email",
                **women,
            },
        ],
        "unit": "percentage points",
        "explanation": (
            "Treatment effects compare each email group "
            "against the randomized No Email control group."
        ),
    }


@app.get("/api/causal")
def causal():
    return get_causal_data()


# --------------------------------------------------
# UPLIFT ANALYSIS
# --------------------------------------------------

def get_uplift_data():

    return {
        "model": "T-learner",
        "model_type": "Uplift modelling",
        "metrics": {
            "qini_coefficient": 0.8665,
            "predicted_mean_uplift": 0.632,
            "observed_test_ate": 0.832,
            "top_20_percent_uplift": 1.313,
            "roc_auc": 0.549,
            "pr_auc": 0.0103,
        },
        "unit": "percentage points for uplift effects",
        "qini_explanation": (
            "Qini measures the ranking quality of an uplift model; "
            "it is not classification accuracy."
        ),
        "source": (
            "Previously evaluated T-learner experiment results. "
            "These metrics are exposed as a cached summary and "
            "are not recalculated on every API request."
        ),
    }


@app.get("/api/uplift")
def uplift():
    return get_uplift_data()


# --------------------------------------------------
# MODEL INSIGHTS
# --------------------------------------------------

def get_model_insights():

    estimator = load_csv(
        REPORTS_DIR,
        "dml_estimator_comparison.csv",
    )

    holdout = load_csv(
        REPORTS_DIR,
        "dml_truth_holdout_validation.csv",
    )

    repeated = load_csv(
        REPORTS_DIR,
        "dml_truth_repeated_seed_summary.csv",
    )

    split_ratios = load_csv(
        REPORTS_DIR,
        "dml_split_ratio_validation.csv",
    )

    configurations = load_csv(
        REPORTS_DIR,
        "dml_model_configuration_summary.csv",
    )

    validate_dataframe(
        estimator,
        "dml_estimator_comparison.csv",
        {
            "estimator",
            "holdout_customers",
            "true_ate",
            "estimated_ate",
            "ate_bias",
            "mae",
            "rmse",
            "effect_correlation",
        },
    )

    validate_dataframe(
        holdout,
        "dml_truth_holdout_validation.csv",
        {
            "holdout_customers",
            "true_ate",
            "estimated_ate",
            "ate_bias",
            "mae",
            "rmse",
            "effect_correlation",
        },
    )

    validate_dataframe(
        repeated,
        "dml_truth_repeated_seed_summary.csv",
        {
            "metric",
            "mean",
            "std",
            "minimum",
            "maximum",
        },
    )

    validate_dataframe(
        split_ratios,
        "dml_split_ratio_validation.csv",
        {
            "training_percentage",
            "testing_percentage",
            "training_customers",
            "holdout_customers",
            "true_ate",
            "estimated_ate",
            "ate_bias",
            "absolute_ate_bias",
            "mae",
            "rmse",
        },
    )

    validate_dataframe(
        configurations,
        "dml_model_configuration_summary.csv",
        {
            "configuration",
            "runs",
            "n_estimators",
            "min_samples_leaf",
            "training_customers_per_run",
            "holdout_customers_per_run",
            "true_ate_mean",
            "true_ate_std",
            "estimated_ate_mean",
            "estimated_ate_std",
            "ate_bias_mean",
            "ate_bias_std",
            "absolute_ate_bias_mean",
            "absolute_ate_bias_std",
            "mae_mean",
            "mae_std",
            "rmse_mean",
            "rmse_std",
            "effect_correlation_mean",
            "effect_correlation_std",
        },
    )

    return {
        "primary_validation": clean_records(holdout)[0],
        "estimator_comparison": clean_records(estimator),
        "repeated_seed_summary": clean_records(repeated),
        "split_ratio_validation": clean_records(split_ratios),
        "configuration_summary": clean_records(configurations),
        "dataset": "Synthetic pricing validation dataset",
        "disclaimer": (
            "Synthetic validation results do not prove "
            "real-world causal effects."
        ),
    }


@app.get("/api/model-insights")
def model_insights():
    return get_model_insights()


# --------------------------------------------------
# DASHBOARD OVERVIEW
# --------------------------------------------------

@app.get("/api/overview")
def overview():

    hillstrom = load_csv(
        DATA_DIR,
        "hillstrom.csv",
    )

    validate_dataframe(
        hillstrom,
        "hillstrom.csv",
        {"segment", "conversion"},
    )

    pricing_results = get_pricing_data()
    causal_results = get_causal_data()
    uplift_results = get_uplift_data()
    model_results = get_model_insights()

    best_policy = pricing_results["best_policy"]
    men_effect = causal_results["effects"][0]
    uplift_metrics = uplift_results["metrics"]

    return {
        "customers_analysed": len(hillstrom),
        "best_discount": best_policy["discount"],
        "expected_profit_per_customer": best_policy["profit"],
        "qini_coefficient": uplift_metrics["qini_coefficient"],
        "mens_email_effect": men_effect["effect"],
        "pricing_dataset_customers": pricing_results["customers"],
        "dml_holdout_ate": (
            model_results["primary_validation"]["estimated_ate"]
        ),
        "data_sources": [
            "Hillstrom randomized email experiment",
            "Synthetic pricing dataset",
            "Synthetic DML validation",
        ],
    }


# --------------------------------------------------
# REPORT EXPORT
# --------------------------------------------------

@app.get(
    "/api/report",
    response_class=PlainTextResponse,
)
def export_report():

    overview_data = overview()
    pricing_data = get_pricing_data()
    causal_data = get_causal_data()
    uplift_data = get_uplift_data()
    model_data = get_model_insights()

    lines = [
        "ECONOCAUSAL DYNAMIC PRICING REPORT",
        "=" * 45,
        "",
        "OVERVIEW",
        f"Customers analysed: {overview_data['customers_analysed']}",
        f"Best tested discount: {overview_data['best_discount']}",
        (
            "Expected profit per customer: "
            f"${overview_data['expected_profit_per_customer']:.2f}"
        ),
        "",
        "PRICING ANALYTICS",
    ]

    for policy in pricing_data["policies"]:
        lines.append(
            f"{policy['discount']}: "
            f"Revenue/customer=${policy['revenue']:.2f}, "
            f"Profit/customer=${policy['profit']:.2f}"
        )

    lines.extend([
        "",
        "CAUSAL ANALYSIS - HILLSTROM",
    ])

    for effect in causal_data["effects"]:
        lines.append(
            f"{effect['segment']}: "
            f"{effect['effect']:.3f} percentage points "
            f"(95% CI: {effect['lower']:.3f} to "
            f"{effect['upper']:.3f})"
        )

    lines.extend([
        "",
        "UPLIFT ANALYSIS",
        f"Qini coefficient: {uplift_data['metrics']['qini_coefficient']}",
        (
            "Predicted mean uplift: "
            f"{uplift_data['metrics']['predicted_mean_uplift']} pp"
        ),
        (
            "Observed top 20% uplift: "
            f"{uplift_data['metrics']['top_20_percent_uplift']} pp"
        ),
        "",
        "MODEL INSIGHTS - DML",
    ])

    for key, value in model_data["primary_validation"].items():
        lines.append(f"{key}: {value}")

    lines.extend([
        "",
        "LIMITATIONS",
        pricing_data["disclaimer"],
        causal_data["explanation"],
        model_data["disclaimer"],
        "",
        "Generated by EconoCausal Dynamic Pricing API",
    ])

    return "\n".join(lines)
