import argparse
from pathlib import Path

from src.validate_data import validate_dataset


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Run dataset quality validation on a CSV file."
    )

    parser.add_argument(
        "dataset",
        type=Path,
        help="Path to the CSV dataset to validate."
    )

    args = parser.parse_args(argv)

    result = validate_dataset(args.dataset)

    return 0 if result else 1


if __name__ == "__main__":
    raise SystemExit(main())
