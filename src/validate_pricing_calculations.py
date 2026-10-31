from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_FILE = PROJECT_ROOT / "data" / "synthetic_pricing.csv"

REQUIRED_COLUMNS = {
    "original_price",
    "discount_rate",
    "discounted_price",
    "units_sold",
    "purchase",
    "revenue",
    "discount_cost",
}


def validate_pricing_calculations(file_path=DEFAULT_DATA_FILE):
    """Check pricing calculations and consistency in a pricing CSV."""

    path = Path(file_path)

    if not path.is_file():
        print(f"ERROR: Dataset not found: {path}")
        return False

    try:
        df = pd.read_csv(path)
    except (OSError, UnicodeDecodeError, pd.errors.ParserError) as error:
        print(f"ERROR: Could not read dataset: {error}")
        return False

    missing_columns = REQUIRED_COLUMNS - set(df.columns)

    if missing_columns:
        print("ERROR: Missing required columns:")
        print(", ".join(sorted(missing_columns)))
        return False

    if df.empty:
        print("ERROR: Dataset is empty.")
        return False

    numeric_columns = sorted(REQUIRED_COLUMNS)
    numeric_data = df[numeric_columns].apply(
        pd.to_numeric, errors="coerce"
    )

    if numeric_data.isna().any().any():
        print("ERROR: Required numeric columns contain missing or invalid values.")
        return False

    if not np.isfinite(numeric_data.to_numpy()).all():
        print("ERROR: Required numeric columns contain non-finite values.")
        return False

    original_price = numeric_data["original_price"]
    discount_rate = numeric_data["discount_rate"]
    discounted_price = numeric_data["discounted_price"]
    units_sold = numeric_data["units_sold"]
    purchase = numeric_data["purchase"]
    revenue = numeric_data["revenue"]
    discount_cost = numeric_data["discount_cost"]

    checks = {
        "Discounted price calculation": np.isclose(
            discounted_price,
            (original_price * (1 - discount_rate)).round(2),
            atol=0.001,
            rtol=0,
        ),
        "Revenue calculation": np.isclose(
            revenue,
            (original_price * (1 - discount_rate) * units_sold).round(2),
            atol=0.001,
            rtol=0,
        ),
        "Discount cost calculation": np.isclose(
            discount_cost,
            (original_price * discount_rate * units_sold).round(2),
            atol=0.001,
            rtol=0,
        ),
        "Purchase and units consistency": (
            (purchase == 1) == (units_sold > 0)
        ),
        "Valid purchase values": purchase.isin([0, 1]),
        "Valid discount rates": discount_rate.between(0, 1),
        "Non-negative prices, quantities, revenue and discount cost": (
            (original_price >= 0)
            & (discounted_price >= 0)
            & (units_sold >= 0)
            & (revenue >= 0)
            & (discount_cost >= 0)
        ),
    }

    print("\nPRICING CALCULATION VALIDATION")
    print("=" * 45)
    print(f"Dataset: {path}")
    print(f"Rows checked: {len(numeric_data)}")
    print()

    all_passed = True

    for name, passed in checks.items():
        failures = int((~passed).sum())
        status = "PASS" if failures == 0 else "FAIL"
        print(f"{status}: {name} — {failures} mismatches")

        if failures:
            all_passed = False

    print("\nFINAL RESULT:", "PASS" if all_passed else "FAIL")
    return all_passed


if __name__ == "__main__":
    success = validate_pricing_calculations()

    if not success:
        raise SystemExit(1)
