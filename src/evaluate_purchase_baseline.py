"""Calculate a descriptive difference-in-means purchase baseline."""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_ROOT / "data" / "synthetic_pricing.csv"
REPORT_FILE = PROJECT_ROOT / "reports" / "purchase_baseline_summary.csv"


def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

    df = pd.read_csv(DATA_FILE)

    required = {"customer_id", "treatment", "purchase"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    if df.empty:
        raise ValueError("Dataset is empty.")

    if df[["customer_id", "treatment", "purchase"]].isna().any().any():
        raise ValueError("Required columns contain missing values.")

    if df["customer_id"].duplicated().any():
        raise ValueError("Customer IDs must be unique.")

    if set(df["treatment"].unique()) != {0, 1}:
        raise ValueError("Treatment must contain both 0 and 1.")

    if not set(df["purchase"].unique()).issubset({0, 1}):
        raise ValueError("Purchase must contain only 0 and 1.")

    grouped = df.groupby("treatment")["purchase"].agg(
        customers="count",
        purchase_rate="mean",
    )

    control_rate = float(grouped.loc[0, "purchase_rate"])
    treated_rate = float(grouped.loc[1, "purchase_rate"])
    difference = treated_rate - control_rate

    summary = pd.DataFrame([
        {
            "metric": "control_purchase_rate",
            "value": control_rate,
        },
        {
            "metric": "treated_purchase_rate",
            "value": treated_rate,
        },
        {
            "metric": "difference_in_means",
            "value": difference,
        },
        {
            "metric": "difference_in_percentage_points",
            "value": difference * 100,
        },
        {
            "metric": "control_customers",
            "value": int(grouped.loc[0, "customers"]),
        },
        {
            "metric": "treated_customers",
            "value": int(grouped.loc[1, "customers"]),
        },
        {
            "metric": "total_customers",
            "value": len(df),
        },
    ])

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(REPORT_FILE, index=False)

    print("Descriptive purchase baseline")
    print("-----------------------------")
    print(f"Control purchase rate: {control_rate:.4%}")
    print(f"Treated purchase rate: {treated_rate:.4%}")
    print(f"Difference: {difference:.6f}")
    print(f"Difference in percentage points: {difference * 100:.4f}")
    print(f"Report saved to: {REPORT_FILE}")
    print("Note: This is an observed difference, not necessarily a causal effect.")


if __name__ == "__main__":
    main()
