import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

import pandas as pd

from src.validate_data import validate_dataset


class TestDataValidation(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.csv_path = Path(self.temp_dir.name) / "test_dataset.csv"

        self.valid_data = pd.DataFrame({
            "customer_id": [101, 102, 103],
            "discount_rate": [0.05, 0.10, 0.0],
            "treatment": [1, 1, 0],
            "purchase": [1, 0, 1],
        })

        self.valid_data.to_csv(self.csv_path, index=False)

    def tearDown(self):
        self.temp_dir.cleanup()

    def run_validator(self):
        output = io.StringIO()

        with redirect_stdout(output):
            result = validate_dataset(self.csv_path)

        return result, output.getvalue()

    def test_valid_dataset_passes(self):
        result, output = self.run_validator()

        self.assertTrue(result)
        self.assertIn("Validation report completed.", output)
        self.assertIn("No missing values found.", output)

    def test_missing_dataset_file_is_detected(self):
        missing_path = Path(self.temp_dir.name) / "missing.csv"

        with redirect_stdout(io.StringIO()) as output:
            result = validate_dataset(missing_path)

        self.assertFalse(result)
        self.assertIn("Dataset file not found", output.getvalue())

    def test_duplicate_rows_are_reported(self):
        duplicate_data = pd.concat(
            [self.valid_data, self.valid_data.iloc[[0]]],
            ignore_index=True,
        )
        duplicate_data.to_csv(self.csv_path, index=False)

        result, output = self.run_validator()

        self.assertTrue(result)
        self.assertIn("Duplicate rows found: 1", output)

    def test_invalid_discount_values_are_reported(self):
        self.valid_data.loc[0, "discount_rate"] = 0.25
        self.valid_data.to_csv(self.csv_path, index=False)

        result, output = self.run_validator()

        self.assertTrue(result)
        self.assertIn("Invalid discount values: 1", output)

    def test_invalid_treatment_values_are_reported(self):
        self.valid_data.loc[0, "treatment"] = 2
        self.valid_data.to_csv(self.csv_path, index=False)

        result, output = self.run_validator()

        self.assertTrue(result)
        self.assertIn("Invalid treatment values: 1", output)

    def test_treatment_discount_inconsistency_is_reported(self):
        self.valid_data.loc[0, "treatment"] = 0
        self.valid_data.to_csv(self.csv_path, index=False)

        result, output = self.run_validator()

        self.assertTrue(result)
        self.assertIn("Treatment-discount inconsistencies: 1", output)

    def test_invalid_purchase_values_are_reported(self):
        self.valid_data.loc[0, "purchase"] = 3
        self.valid_data.to_csv(self.csv_path, index=False)

        result, output = self.run_validator()

        self.assertTrue(result)
        self.assertIn("Invalid purchase values: 1", output)

    def test_missing_customer_ids_are_reported(self):
        self.valid_data.loc[0, "customer_id"] = None
        self.valid_data.to_csv(self.csv_path, index=False)

        result, output = self.run_validator()

        self.assertTrue(result)
        self.assertIn("Missing customer IDs: 1", output)


if __name__ == "__main__":
    unittest.main()