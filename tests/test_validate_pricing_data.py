
import pandas as pd

from src.data_processing.validate_pricing_data import validate_pricing_data


def make_valid_data():
    return pd.DataFrame({
        "customer_id": [1, 2],
        "age": [22, 35],
        "income": [25000.0, 40000.0],
        "past_purchases": [2, 3],
        "product_category": ["Clothing", "Electronics"],
        "original_price": [100.0, 200.0],
        "discount_rate": [0.10, 0.20],
        "treatment": [1, 1],
        "purchase": [1, 0],
        "units_sold": [1, 0],
        "discounted_price": [90.0, 160.0],
        "revenue": [90.0, 0.0],
        "discount_cost": [10.0, 0.0],
        "purchase_probability": [0.7, 0.3],
    })


def test_valid_data_has_no_issues():
    df = make_valid_data()
    assert validate_pricing_data(df) == []


def test_missing_required_column_is_reported():
    df = make_valid_data().drop(columns=["income"])
    issues = validate_pricing_data(df)
    assert any("Missing required columns" in issue for issue in issues)


def test_discount_outside_valid_range_is_reported():
    df = make_valid_data()
    df.loc[0, "discount_rate"] = 1.2
    issues = validate_pricing_data(df)
    assert any("discount_rate" in issue for issue in issues)


def test_duplicate_customer_ids_are_reported():
    df = make_valid_data()
    df.loc[1, "customer_id"] = df.loc[0, "customer_id"]
    issues = validate_pricing_data(df)
    assert any("Duplicate customer_id" in issue for issue in issues)


def test_inconsistent_discounted_price_is_reported():
    df = make_valid_data()
    df.loc[0, "discounted_price"] = 95.0
    issues = validate_pricing_data(df)
    assert any("Discounted prices" in issue for issue in issues)

def test_empty_dataset_is_reported():
    df = make_valid_data().iloc[0:0]
    issues = validate_pricing_data(df)

    assert "Dataset is empty." in issues

def test_missing_values_are_reported():
    df = make_valid_data()
    df.loc[0, "income"] = None

    issues = validate_pricing_data(df)

    assert any("missing values" in issue.lower() for issue in issues)


def test_invalid_treatment_value_is_reported():
    df = make_valid_data()
    df.loc[0, "treatment"] = 2

    issues = validate_pricing_data(df)

    assert any("treatment" in issue for issue in issues)


def test_invalid_purchase_value_is_reported():
    df = make_valid_data()
    df.loc[0, "purchase"] = 3

    issues = validate_pricing_data(df)

    assert any("purchase" in issue for issue in issues)


def test_boundary_discount_rates_are_accepted():
    df = make_valid_data()
    df.loc[0, "discount_rate"] = 0.0
    df.loc[0, "discounted_price"] = 100.0
    df.loc[1, "discount_rate"] = 1.0
    df.loc[1, "discounted_price"] = 0.0

    issues = validate_pricing_data(df)

    assert not any("discount_rate" in issue for issue in issues)
    assert not any("Discounted prices" in issue for issue in issues)

def test_non_numeric_income_is_reported():
    df = make_valid_data()
    df["income"] = df["income"].astype(object)
    df.loc[0, "income"] = "invalid"

    issues = validate_pricing_data(df)

    assert any("numeric" in issue.lower() for issue in issues)


def test_blank_product_category_is_reported():
    df = make_valid_data()
    df.loc[0, "product_category"] = "   "

    issues = validate_pricing_data(df)

    assert any("product_category" in issue for issue in issues)


def test_negative_discounted_price_is_reported():
    df = make_valid_data()
    df.loc[0, "discounted_price"] = -10.0

    issues = validate_pricing_data(df)

    assert any("discounted_price" in issue for issue in issues)