
import pandas as pd


def validate_hillstrom_data(df: pd.DataFrame) -> pd.DataFrame:
    """Validate the required columns in the Hillstrom dataset."""
    required_columns = [
        "recency",
        "history_segment",
        "history",
        "mens",
        "womens",
        "zip_code",
        "newbie",
        "channel",
        "segment",
        "visit",
        "conversion",
        "spend",
    ]

    missing_columns = set(required_columns) - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    if df.empty:
        raise ValueError("The dataset is empty.")

    return df.copy()
