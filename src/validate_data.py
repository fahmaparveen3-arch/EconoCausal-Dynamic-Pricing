from pathlib import Path

import pandas as pd


def validate_dataset(file_path):
    """Validate a pricing dataset and report common data-quality issues."""

    path = Path(file_path)

    if not path.is_file():
        print(f"Error: Dataset file not found: {path}")
        return False

    try:
        df = pd.read_csv(path)
    except (OSError, UnicodeDecodeError, pd.errors.ParserError) as error:
        print(f"Error reading dataset: {error}")
        return False

    print("\nDATASET VALIDATION REPORT")
    print("=" * 40)

    # 1. Basic dataset information
    print(f"File: {path}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"Duplicate rows: {df.duplicated().sum()}")
    print(f"Total missing values: {df.isna().sum().sum()}")

    # 2. Column data types
    print("\nCOLUMN DATA TYPES")
    print("-" * 40)
    print(df.dtypes.to_string())

    # 3. Missing values by column
    print("\nMISSING VALUES BY COLUMN")
    print("-" * 40)

    missing = df.isna().sum()
    missing = missing[missing > 0]

    if missing.empty:
        print("No missing values found.")
    else:
        print(missing.to_string())

    # 4. Duplicate rows
    duplicate_count = int(df.duplicated().sum())
    print("\nDUPLICATE ROW CHECK")
    print("-" * 40)
    print(f"Duplicate rows found: {duplicate_count}")

    # 5. Discount validation
    print("\nDISCOUNT VALIDATION")
    print("-" * 40)

    discount_column = next(
        (
            column
            for column in df.columns
            if column.lower() in {
                "discount",
                "discount_level",
                "discount_rate",
            }
        ),
        None,
    )

    if discount_column is None:
        print("Skipped: No recognised discount column found.")
    else:
        discounts = pd.to_numeric(
            df[discount_column], errors="coerce"
        )

        if discount_column.lower() == "discount_rate":
            # The project stores discount rates as proportions.
            allowed_discounts = {0.00, 0.05, 0.10, 0.15, 0.20}
        else:
            allowed_discounts = {0, 5, 10, 15, 20}

        invalid_discounts = (
            discounts.isna()
            | ~discounts.isin(allowed_discounts)
        )

        observed = sorted(discounts.dropna().unique().tolist())

        print(f"Column checked: {discount_column}")
        print(f"Observed values: {observed}")
        print(f"Invalid discount values: {int(invalid_discounts.sum())}")

    # 6. Purchase outcome validation
    print("\nPURCHASE OUTCOME VALIDATION")
    print("-" * 40)

    if "purchase" in df.columns:
        purchase = pd.to_numeric(df["purchase"], errors="coerce")

        invalid_purchase = (
            purchase.isna() | ~purchase.isin({0, 1})
        )

        print(f"Invalid purchase values: {int(invalid_purchase.sum())}")
    else:
        print("Skipped: No 'purchase' column found.")

    # 7. Customer identifier check
    print("\nCUSTOMER IDENTIFIER CHECK")
    print("-" * 40)

    if "customer_id" in df.columns:
        missing_ids = int(df["customer_id"].isna().sum())
        unique_ids = int(df["customer_id"].nunique())

        print(f"Unique customer IDs: {unique_ids}")
        print(f"Missing customer IDs: {missing_ids}")
    else:
        print("Skipped: No 'customer_id' column found.")

    # 8. Final summary
    print("\nVALIDATION SUMMARY")
    print("=" * 40)

    total_missing = int(df.isna().sum().sum())

    print(f"Rows checked: {len(df)}")
    print(f"Columns checked: {len(df.columns)}")
    print(f"Duplicate rows: {duplicate_count}")
    print(f"Missing values: {total_missing}")

    print("\nValidation report completed.")
    print("Review any reported issues before using the data.")

    return True


if __name__ == "__main__":
    dataset_path = input(
        "Enter the path to your pricing CSV file: "
    ).strip().strip('"')

    validate_dataset(dataset_path)

