
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"


def load_pricing_data() -> pd.DataFrame:
    """Load the synthetic retail pricing dataset."""
    file_path = DATA_DIR / "synthetic_pricing.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            f"Pricing dataset not found at {file_path}. "
            "Run generate_synthetic_pricing_data.py first."
        )

    return pd.read_csv(file_path)


if __name__ == "__main__":
    df = load_pricing_data()

    print("Dataset shape:", df.shape)
    print("\nColumns:")
    print(df.columns.tolist())

    print("\nMissing values:", df.isna().sum().sum())
    print("\nFirst five rows:")
    print(df.head())
