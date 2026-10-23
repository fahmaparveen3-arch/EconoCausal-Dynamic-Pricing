
from pathlib import Path

import pandas as pd

from load_pricing_data import load_pricing_data


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_FILE = DATA_DIR / "prepared_pricing.csv"


def prepare_pricing_data() -> pd.DataFrame:
    """Validate and prepare synthetic pricing data for causal analysis."""
    df = load_pricing_data()

    required_columns = [
        "customer_id",
        "age",
        "income",
        "past_purchases",
        "product_category",
        "original_price",
        "discount_rate",
        "treatment",
        "purchase",
    ]

    missing_columns = [
        column for column in required_columns if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    if df.empty:
        raise ValueError("The pricing dataset is empty.")

    if df["customer_id"].duplicated().any():
        raise ValueError("Duplicate customer IDs found.")

    if df[["treatment", "purchase"]].isna().any().any():
        raise ValueError("Treatment or purchase contains missing values.")

    if not df["treatment"].isin([0, 1]).all():
        raise ValueError("Treatment must contain only 0 and 1.")

    if not df["purchase"].isin([0, 1]).all():
        raise ValueError("Purchase must contain only 0 and 1.")

    if not df.loc[df["treatment"] == 0, "discount_rate"].eq(0).all():
        raise ValueError("Control customers should have a zero discount.")

    if not df.loc[df["treatment"] == 1, "discount_rate"].gt(0).all():
        raise ValueError("Treated customers should have a positive discount.")

    return df


if __name__ == "__main__":
    prepared_df = prepare_pricing_data()
    prepared_df.to_csv(OUTPUT_FILE, index=False)

    print("Data preparation validation successful!")
    print("Dataset shape:", prepared_df.shape)
    print("Saved to:", OUTPUT_FILE)
    print("\nTreatment counts:")
    print(prepared_df["treatment"].value_counts().sort_index())
    print("\nPurchase rate by treatment:")
    print(prepared_df.groupby("treatment")["purchase"].mean())
