import pytest

from src.pricing.dynamic_pricing import (
    calculate_discounted_price,
    calculate_expected_profit,
    compare_candidate_discounts,
    estimate_purchase_probability,
)


def test_calculate_discounted_price():
    assert calculate_discounted_price(100, 0.15) == 85.00


def test_zero_discount():
    assert calculate_discounted_price(100, 0) == 100.00


def test_full_discount():
    assert calculate_discounted_price(100, 1) == 0.00


def test_negative_price_raises_error():
    with pytest.raises(ValueError):
        calculate_discounted_price(-10, 0.15)


def test_invalid_discount_raises_error():
    with pytest.raises(ValueError):
        calculate_discounted_price(100, 1.5)


def test_negative_discount_raises_error():
    with pytest.raises(ValueError):
        calculate_discounted_price(100, -0.1)


def test_negative_price_with_zero_discount_raises_error():
    with pytest.raises(ValueError):
        calculate_discounted_price(-10, 0)


def test_estimate_purchase_probability():
    probability = estimate_purchase_probability(
        age=30,
        income=40000,
        past_purchases=3,
        product_category="Clothing",
        discount_rate=0.10,
    )

    assert 0 <= probability <= 1


def test_estimate_purchase_probability_matches_formula():
    probability = estimate_purchase_probability(
        age=30,
        income=40000,
        past_purchases=3,
        product_category="Clothing",
        discount_rate=0.10,
    )

    assert probability == pytest.approx(0.1616502941, abs=1e-8)


def test_calculate_expected_profit():
    profit = calculate_expected_profit(
        original_price=100,
        age=30,
        income=40000,
        past_purchases=3,
        product_category="Clothing",
        discount_rate=0.10,
    )

    assert profit == pytest.approx(6.466011764, abs=1e-7)


def test_expected_profit_rejects_zero_price():
    with pytest.raises(ValueError):
        calculate_expected_profit(
            original_price=0,
            age=30,
            income=40000,
            past_purchases=3,
            product_category="Clothing",
            discount_rate=0.10,
        )


def test_compare_candidate_discounts():
    results = compare_candidate_discounts(
        original_price=100,
        age=30,
        income=40000,
        past_purchases=3,
        product_category="Clothing",
    )

    assert len(results) == 5

    assert results == sorted(
        results,
        key=lambda result: result["expected_profit"],
        reverse=True,
    )

    assert {result["discount_rate"] for result in results} == {
        0.00, 0.05, 0.10, 0.15, 0.20
    }