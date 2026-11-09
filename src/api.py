
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException

from src.validate_data import validate_dataset
from src.validate_pricing_calculations import validate_pricing_calculations


DATA_DIR = Path(__file__).resolve().parent.parent / "data"

app = FastAPI(
    title="EconoCausal Validation API",
    description="API for dataset quality, pricing validation, and overview metrics.",
    version="1.1.0",
)


def get_dataset_path(filename: str) -> Path:
    if Path(filename).name != filename or Path(filename).suffix.lower() != ".csv":
        raise HTTPException(
            status_code=400,
            detail="Please provide a valid CSV filename.",
        )

    dataset_path = (DATA_DIR / filename).resolve()

    if dataset_path.parent != DATA_DIR.resolve():
        raise HTTPException(status_code=400, detail="Invalid dataset path.")

    if not dataset_path.is_file():
        raise HTTPException(status_code=404, detail="Dataset not found.")

    return dataset_path


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "EconoCausal Validation API",
    }


@app.get("/api/overview")
def overview():
    """Return overview metrics calculated from the synthetic pricing dataset."""

    dataset_path = get_dataset_path("synthetic_pricing.csv")

    try:
        df = pd.read_csv(dataset_path)
    except (OSError, UnicodeDecodeError, pd.errors.ParserError) as error:
        raise HTTPException(
            status_code=500,
            detail=f"Could not read pricing dataset: {error}",
        ) from error

    required_columns = {
        "customer_id",
        "treatment",
        "purchase",
        "discount_rate",
        "revenue",
        "discount_cost",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise HTTPException(
            status_code=422,
            detail=f"Dataset is missing required columns: {sorted(missing_columns)}",
        )

    if df.empty:
        raise HTTPException(
            status_code=422,
            detail="Pricing dataset is empty.",
        )

    numeric_columns = [
        "treatment",
        "purchase",
        "discount_rate",
        "revenue",
        "discount_cost",
    ]

    numeric_data = df[numeric_columns].apply(
        pd.to_numeric,
        errors="coerce",
    )

    if numeric_data.isna().any().any():
        raise HTTPException(
            status_code=422,
            detail="Dataset contains missing or invalid metric values.",
        )

    df[numeric_columns] = numeric_data

    if not df["treatment"].isin([0, 1]).all():
        raise HTTPException(
            status_code=422,
            detail="Treatment values must be 0 or 1.",
        )

    if not df["purchase"].isin([0, 1]).all():
        raise HTTPException(
            status_code=422,
            detail="Purchase values must be 0 or 1.",
        )

    if not df["discount_rate"].between(0, 1).all():
        raise HTTPException(
            status_code=422,
            detail="Discount rates must be between 0 and 1.",
        )

    grouped = df.groupby("treatment")["purchase"].agg(
        customers="count",
        purchase_rate="mean",
    )

    if set(grouped.index) != {0, 1}:
        raise HTTPException(
            status_code=422,
            detail="Dataset must contain both control and treated customers.",
        )

    control_rate = float(grouped.loc[0, "purchase_rate"])
    treated_rate = float(grouped.loc[1, "purchase_rate"])

    discount_groups = (
        df.groupby("discount_rate")["purchase"]
        .agg(
            customers="count",
            purchase_rate="mean",
        )
        .reset_index()
        .sort_values("discount_rate")
    )

    discount_levels = [
        {
            "discount_percent": round(float(row.discount_rate) * 100, 2),
            "customers": int(row.customers),
            "purchase_rate_percent": round(
                float(row.purchase_rate) * 100, 2
            ),
        }
        for row in discount_groups.itertuples(index=False)
    ]

    return {
        "data_source": "synthetic_pricing.csv",
        "data_type": "synthetic",
        "total_customers": int(len(df)),
        "overall_purchase_rate_percent": round(
            float(df["purchase"].mean()) * 100, 2
        ),
        "purchase_baseline": {
            "control_customers": int(grouped.loc[0, "customers"]),
            "treated_customers": int(grouped.loc[1, "customers"]),
            "control_purchase_rate_percent": round(
                control_rate * 100, 2
            ),
            "treated_purchase_rate_percent": round(
                treated_rate * 100, 2
            ),
            "observed_difference_percentage_points": round(
                (treated_rate - control_rate) * 100, 2
            ),
            "interpretation": (
                "Observed difference between groups; "
                "not necessarily a causal effect."
            ),
        },
        "discount_analysis": discount_levels,
        "financial_totals": {
            "total_revenue": round(float(df["revenue"].sum()), 2),
            "total_discount_cost": round(
                float(df["discount_cost"].sum()), 2
            ),
        },
        "limitations": (
            "Metrics are calculated from simulated customer data "
            "and do not establish real-world pricing performance."
        ),
    }


@app.get("/api/validation/dataset/{filename}")
def dataset_validation(filename: str):
    dataset_path = get_dataset_path(filename)

    output = StringIO()

    with redirect_stdout(output):
        completed = validate_dataset(dataset_path)

    return {
        "filename": filename,
        "completed": bool(completed),
        "report": output.getvalue(),
    }


@app.get("/api/validation/pricing/{filename}")
def pricing_validation(filename: str):
    dataset_path = get_dataset_path(filename)

    output = StringIO()

    with redirect_stdout(output):
        passed = validate_pricing_calculations(dataset_path)

    return {
        "filename": filename,
        "passed": bool(passed),
        "report": output.getvalue(),
    }
