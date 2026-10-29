
import numpy as np
import pandas as pd
import pytest

from src.models.train_dml import (
    validate_dml_data,
    fit_dml_model,
    evaluate_dml_holdout,
)


@pytest.fixture
def sample_dml_data():
    """Create a small dataset for testing the DML model."""
    rng = np.random.default_rng(42)
    n = 120

    treatment = np.tile([0, 1], n // 2)
    rng.shuffle(treatment)

    age = rng.integers(18, 71, size=n)
    income = rng.integers(20000, 100001, size=n)
    past_purchases = rng.integers(0, 11, size=n)
    product_category = rng.choice(
        ["Electronics", "Clothing", "Home", "Beauty"],
        size=n,
    )

    probability = 1 / (
        1 + np.exp(
            -(
                -2
                + 0.025 * (age - 40)
                + 0.000015 * (income - 45000)
                + 0.12 * past_purchases
                + 0.8 * treatment
            )
        )
    )

    purchase = rng.binomial(1, probability)

    # Ensure both outcome classes are present for this test dataset.
    purchase[0] = 0
    purchase[1] = 1

    return pd.DataFrame(
        {
            "customer_id": np.arange(1, n + 1),
            "age": age,
            "income": income,
            "past_purchases": past_purchases,
            "product_category": product_category,
            "treatment": treatment,
            "purchase": purchase,
        }
    )


def test_validate_dml_data_accepts_valid_data(sample_dml_data):
    validate_dml_data(sample_dml_data)


def test_validate_dml_data_rejects_missing_column(sample_dml_data):
    invalid_data = sample_dml_data.drop(columns=["income"])

    with pytest.raises(ValueError, match="Missing required columns"):
        validate_dml_data(invalid_data)


def test_validate_dml_data_rejects_duplicate_customer_ids(
    sample_dml_data,
):
    invalid_data = sample_dml_data.copy()
    invalid_data.loc[1, "customer_id"] = invalid_data.loc[0, "customer_id"]

    with pytest.raises(ValueError, match="Customer IDs must be unique"):
        validate_dml_data(invalid_data)


def test_validate_dml_data_rejects_invalid_treatment(sample_dml_data):
    invalid_data = sample_dml_data.copy()
    invalid_data.loc[0, "treatment"] = 2

    with pytest.raises(ValueError, match="Treatment must contain only 0 and 1"):
        validate_dml_data(invalid_data)


def test_fit_dml_model_returns_finite_customer_effects(sample_dml_data):
    model, results = fit_dml_model(sample_dml_data)

    assert len(results) == len(sample_dml_data)
    assert results["customer_id"].tolist() == (
        sample_dml_data["customer_id"].tolist()
    )
    assert np.isfinite(
        results["estimated_discount_effect"].to_numpy()
    ).all()

def test_evaluate_dml_holdout_returns_valid_test_customers(
    sample_dml_data,
):
    results = evaluate_dml_holdout(sample_dml_data, test_size=0.25)

    expected_test_size = int(len(sample_dml_data) * 0.25)

    assert len(results) == expected_test_size
    assert results["customer_id"].nunique() == expected_test_size
    assert results["customer_id"].isin(
        sample_dml_data["customer_id"]
    ).all()
    assert np.isfinite(
        results["estimated_discount_effect"].to_numpy()
    ).all()

@pytest.mark.parametrize(
    ("column", "value", "message"),
    [
        ("age", np.nan, "non-finite values"),
        ("income", np.inf, "non-finite values"),
        ("income", -100, "Income cannot be negative"),
        ("age", 17, "Age must be between 18 and 70"),
        ("age", 71, "Age must be between 18 and 70"),
        ("past_purchases", -1, "Past purchases cannot be negative"),
    ],
)

def test_validate_dml_data_rejects_invalid_numeric_values(
    sample_dml_data, column, value, message
):
    invalid_data = sample_dml_data.copy()

    if column == "income" and np.isinf(value):
        invalid_data["income"] = invalid_data["income"].astype(float)

    if pd.isna(value):
        expected_message = "missing values"
    else:
        expected_message = message

    invalid_data.loc[0, column] = value

    with pytest.raises(ValueError, match=expected_message):
        validate_dml_data(invalid_data)



def test_validate_dml_data_rejects_missing_treatment(
    sample_dml_data,
):
    invalid_data = sample_dml_data.copy()
    invalid_data.loc[0, "treatment"] = np.nan

    with pytest.raises(ValueError, match="missing values"):
        validate_dml_data(invalid_data)


def test_validate_dml_data_rejects_missing_purchase(
    sample_dml_data,
):
    invalid_data = sample_dml_data.copy()
    invalid_data.loc[0, "purchase"] = np.nan

    with pytest.raises(ValueError, match="missing values"):
        validate_dml_data(invalid_data)
