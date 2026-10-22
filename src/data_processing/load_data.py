
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"


def load_hillstrom_data() -> pd.DataFrame:
    """Load the Hillstrom email campaign dataset from a local CSV file."""
    file_path = DATA_DIR / "hillstrom.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {file_path}. "
            "Place the approved Hillstrom CSV file in the data folder."
        )

    return pd.read_csv(file_path)


if __name__ == "__main__":
    df = load_hillstrom_data()
    print("Dataset shape:", df.shape)
    print(df.head())
