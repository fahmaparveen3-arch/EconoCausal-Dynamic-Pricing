import numpy as np
import pandas as pd
import pytest

from src.evaluation.compare_discount_causal_effects import (
    prepare_discount_comparison_data,
    evaluate_discount_level,
)


@pytest.fixture
def sample_pricing_data():
    """Create a small dataset containing control and four discount arms."""
    rng = np.random.default_rng(42)
    rows = []

    for discount in [0.00, 0.05, 0.10, 0.15, 0.20]:
        for i in range(40):
            age = int(rng.integers(18, 71))
            income = int(rng.integers(20000, 100001))
            past_purchases = int(rng.integers(0, 11))
            category = str(
                rng.choice(["Electronics", "Clothing", "Home", "Beauty"])
            )

            rows.append({
                "customer_id": len(rows) + 1,
                "age": age,
                "income": income,
                "past_purchases": past_purchases,
                "product_category": category,
                "discount_rate": discount,
                "treatment": int(discount > 0),
                "purchase": int(rng.binomial(1, 0.3)),
            })

    return pd.DataFrame(rows)


@pytest.mark.parametrize("discount", [0.05, 0.10, 0.15, 0.20])
def test_prepare_discount_comparison_uses_only_selected_arm_and_control(
    sample_pricing_data, discount
):
    comparison = prepare_discount_comparison_data(
        sample_pricing_data, discount
    )

    assert set(comparison["discount_rate"].unique()) == {0.0, discount}
    assert set(comparison["treatment"].unique()) == {0, 1}
    assert (comparison.loc[
        comparison["treatment"] == 0, "discount_rate"
    ] == 0.0).all()
    assert (comparison.loc[
        comparison["treatment"] == 1, "discount_rate"
    ] == discount).all()


def test_prepare_discount_comparison_rejects_unsupported_level(
    sample_pricing_data,
):
    with pytest.raises(ValueError, match="Unsupported discount level"):
        prepare_discount_comparison_data(sample_pricing_data, 0.12)


def test_prepare_discount_comparison_rejects_missing_discount_arm(
    sample_pricing_data,
):
    data = sample_pricing_data[
        sample_pricing_data["discount_rate"] != 0.10
    ]

    with pytest.raises(ValueError, match="Both control and 10% discount"):
        prepare_discount_comparison_data(data, 0.10)


def test_evaluate_discount_level_calculates_holdout_metrics(
    sample_pricing_data, monkeypatch
):
    from src.evaluation import compare_discount_causal_effects as module

    def fake_holdout(comparison):
        # Return one finite estimate for every comparison customer.
        return pd.DataFrame({
            "customer_id": comparison["customer_id"].to_numpy(),
            "estimated_discount_effect": np.full(len(comparison), 0.05),
        })

    monkeypatch.setattr(module, "evaluate_dml_holdout", fake_holdout)

    result = evaluate_discount_level(sample_pricing_data, 0.05)

    assert result["discount_rate"] == 0.05
    assert result["control_customers"] == 40
    assert result["discount_customers"] == 40
    assert result["holdout_customers"] == 80
    assert np.isfinite(result["true_ate"])
    assert np.isfinite(result["estimated_ate"])
    assert np.isfinite(result["ate_bias"])
    assert np.isfinite(result["individual_effect_mae"])
    assert np.isfinite(result["individual_effect_rmse"])