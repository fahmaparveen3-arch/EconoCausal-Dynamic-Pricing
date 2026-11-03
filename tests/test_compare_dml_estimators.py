import numpy as np
import pandas as pd
import pytest

from src.evaluation.compare_dml_estimators import (
    estimate_difference_in_means,
    calculate_baseline_metrics,
    calculate_metrics,
)


def sample_training_data():
    return pd.DataFrame(
        {
            "treatment": [0, 0, 1, 1],
            "purchase": [0, 1, 1, 1],
        }
    )


def test_difference_in_means_calculates_correct_ate():
    df = sample_training_data()

    result = estimate_difference_in_means(df)

    assert result == pytest.approx(0.5)


def test_difference_in_means_rejects_missing_treatment_group():
    df = pd.DataFrame(
        {
            "treatment": [0, 0, 0],
            "purchase": [0, 1, 0],
        }
    )

    with pytest.raises(ValueError, match="Both treatment and control"):
        estimate_difference_in_means(df)


def test_baseline_metrics_calculate_correct_ate_bias():
    df = sample_training_data()
    truth = [0.1, 0.2]

    result = calculate_baseline_metrics(df, truth)

    assert result["true_ate"] == pytest.approx(0.15)
    assert result["estimated_ate"] == pytest.approx(0.5)
    assert result["ate_bias"] == pytest.approx(0.35)
    assert result["absolute_ate_bias"] == pytest.approx(0.35)


def test_baseline_does_not_report_individual_effect_metrics():
    df = sample_training_data()

    result = calculate_baseline_metrics(df, [0.1, 0.2])

    assert np.isnan(result["mae"])
    assert np.isnan(result["rmse"])
    assert np.isnan(result["effect_correlation"])


def test_dml_metrics_include_absolute_ate_bias():
    truth = np.array([0.1, 0.2, 0.3])
    estimates = np.array([0.2, 0.3, 0.4])

    result = calculate_metrics(truth, estimates)

    assert result["ate_bias"] == pytest.approx(0.1)
    assert result["absolute_ate_bias"] == pytest.approx(0.1)