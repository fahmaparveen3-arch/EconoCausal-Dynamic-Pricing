

"""Validation utilities for the EconoCausal pricing dataset."""

import pandas as pd


REQUIRED_COLUMNS = {
    "customer_id",
    "age",
    "income",
    "past_purchases",
    "product_category",
    "original_price",
    "discount_rate",
    "treatment",
    "purchase",
    "units_sold",
    "discounted_price",
    "revenue",
    "discount_cost",
    "purchase_probability",
}

NUMERIC_COLUMNS = {
    "age",
    "income",
    "past_purchases",
    "original_price",
    "discount_rate",
    "treatment",
    "purchase",
    "units_sold",
    "discounted_price",
    "revenue",
    "discount_cost",
    "purchase_probability",
}


def validate_pricing_data(df: pd.DataFrame) -> list[str]:
    """Return a list of validation issues; an empty list means valid."""
    issues = []

    missing_columns = REQUIRED_COLUMNS - set(df.columns)
    if missing_columns:
        issues.append(
            f"Missing required columns: {', '.join(sorted(missing_columns))}"
        )
        return issues

    if df.empty:
        issues.append("Dataset is empty.")
        return issues

    if df[list(REQUIRED_COLUMNS)].isnull().any().any():
        issues.append("Required columns contain missing values.")

    if df["customer_id"].duplicated().any():
        issues.append("Duplicate customer_id values found.")

    # Check that numeric columns contain numeric data.
    invalid_numeric_columns = []

    for column in NUMERIC_COLUMNS:
        if not pd.api.types.is_numeric_dtype(df[column]):
            issues.append(f"{column} must contain numeric values.")
            invalid_numeric_columns.append(column)

    # Check product categories for blank values.
    if not df["product_category"].astype(str).str.strip().ne("").all():
        issues.append("product_category cannot contain blank values.")

    # Stop numeric comparisons for columns containing non-numeric data.
    if invalid_numeric_columns:
        return issues

    if (df["age"] <= 0).any():
        issues.append("Age must be greater than zero.")

    if (df["income"] < 0).any():
        issues.append("Income cannot be negative.")

    if (df["past_purchases"] < 0).any():
        issues.append("past_purchases cannot be negative.")

    if (df["original_price"] <= 0).any():
        issues.append("Original prices must be greater than zero.")

    if not df["discount_rate"].between(0, 1).all():
        issues.append("discount_rate must be between 0 and 1.")

    if (df["discounted_price"] < 0).any():
        issues.append("discounted_price cannot be negative.")

    expected_prices = (
        df["original_price"] * (1 - df["discount_rate"])
    ).round(2)

    if not (
        (df["discounted_price"] - expected_prices).abs() <= 0.011
    ).all():
        issues.append("Discounted prices do not match the discount rates.")

    # Validate revenue calculations.
    expected_revenue = (
        df["discounted_price"] * df["units_sold"]
    ).round(2)

    if not (
        (df["revenue"] - expected_revenue).abs() <= 0.01
    ).all():
        issues.append("Revenue does not match discounted price multiplied by units sold.")

    # Validate discount cost calculations.
    expected_discount_cost = (
        (df["original_price"] - df["discounted_price"])
        * df["units_sold"]
    ).round(2)

    if not (
        (df["discount_cost"] - expected_discount_cost).abs() <= 0.01
    ).all():
        issues.append("Discount cost does not match the calculated discount amount.")

    if not df["treatment"].isin([0, 1]).all():
        issues.append("treatment must contain only 0 or 1.")

    if not df["purchase"].isin([0, 1]).all():
        issues.append("purchase must contain only 0 or 1.")

    if not df["purchase_probability"].between(0, 1).all():
        issues.append("purchase_probability must be between 0 and 1.")

    if (df["units_sold"] < 0).any():
        issues.append("units_sold cannot be negative.")

    if (df["revenue"] < 0).any():
        issues.append("revenue cannot be negative.")

    if (df["discount_cost"] < 0).any():
        issues.append("discount_cost cannot be negative.")

    return issues
