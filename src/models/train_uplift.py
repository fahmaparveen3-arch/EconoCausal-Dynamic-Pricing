
"""Starter module for uplift modelling."""

from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline


def create_uplift_model(preprocessor, random_state=42):
    """Create a Random Forest model for conversion prediction."""
    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=300,
                    min_samples_leaf=20,
                    random_state=random_state,
                    n_jobs=-1,
                ),
            ),
        ]
    )
