
"""Evaluation helpers for uplift modelling."""

import numpy as np
from sklearn.metrics import average_precision_score, roc_auc_score


def evaluate_conversion_model(y_true, y_probability):
    """Evaluate conversion probabilities for a binary classifier."""
    results = {
        "conversion_rate": float(np.mean(y_true)),
        "average_precision": float(
            average_precision_score(y_true, y_probability)
        ),
    }

    if len(np.unique(y_true)) == 2:
        results["roc_auc"] = float(
            roc_auc_score(y_true, y_probability)
        )
    else:
        results["roc_auc"] = float("nan")

    return results
