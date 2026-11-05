import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

import pandas as pd

from src.validate_pricing_calculations import (
    validate_pricing_calculations,
)


class TestPricingCalculations(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.csv_path = Path(self.temp_dir.name) / "test_pricing.csv"

        self.valid_data = pd.DataFrame({
            "original_price": [100.0, 50.0],
            "discount_rate": [0.10, 0.0],
            "discounted_price": [90.0, 50.0],
            "units_sold": [2, 1],
            "purchase": [1, 1],
            "revenue": [180.0, 50.0],
            "discount_cost": [20.0, 0.0],
        })

        self.valid_data.to_csv(self.csv_path, index=False)

    def tearDown(self):
        self.temp_dir.cleanup()

    def run_validator(self):
        output = io.StringIO()

        with redirect_stdout(output):
            result = validate_pricing_calculations(self.csv_path)

        return result, output.getvalue()

    def test_valid_pricing_data_passes(self):
        result, output = self.run_validator()

        self.assertTrue(result)
        self.assertIn("FINAL RESULT: PASS", output)

    def test_incorrect_revenue_is_detected(self):
        self.valid_data.loc[0, "revenue"] = 181.0
        self.valid_data.to_csv(self.csv_path, index=False)

        result, output = self.run_validator()

        self.assertFalse(result)
        self.assertIn("FAIL: Revenue calculation", output)

    def test_invalid_discount_rate_is_detected(self):
        self.valid_data.loc[0, "discount_rate"] = 1.2
        self.valid_data.loc[0, "discounted_price"] = -20.0
        self.valid_data.loc[0, "revenue"] = -40.0
        self.valid_data.loc[0, "discount_cost"] = 240.0
        self.valid_data.to_csv(self.csv_path, index=False)

        result, output = self.run_validator()

        self.assertFalse(result)
        self.assertIn("FAIL: Valid discount rates", output)

    def test_missing_required_column_is_detected(self):
        self.valid_data.drop(columns=["discount_cost"]).to_csv(
            self.csv_path, index=False
        )

        result, output = self.run_validator()

        self.assertFalse(result)
        self.assertIn("Missing required columns", output)
    
    def test_missing_dataset_file_is_detected(self):
        missing_path = Path(self.temp_dir.name) / "missing.csv"

        with redirect_stdout(io.StringIO()) as output:
            result = validate_pricing_calculations(missing_path)

        self.assertFalse(result)
        self.assertIn("Dataset not found", output.getvalue())

    def test_empty_dataset_is_detected(self):
        empty_data = pd.DataFrame(columns=self.valid_data.columns)
        empty_data.to_csv(self.csv_path, index=False)

        result, output = self.run_validator()

        self.assertFalse(result)
        self.assertIn("Dataset is empty", output)

    def test_missing_numeric_values_are_detected(self):
        self.valid_data.loc[0, "revenue"] = float("nan")
        self.valid_data.to_csv(self.csv_path, index=False)

        result, output = self.run_validator()

        self.assertFalse(result)
        self.assertIn("missing or invalid values", output)

    def test_non_finite_values_are_detected(self):
        self.valid_data.loc[0, "original_price"] = float("inf")
        self.valid_data.to_csv(self.csv_path, index=False)

        result, output = self.run_validator()

        self.assertFalse(result)
        self.assertIn("non-finite values", output)

if __name__ == "__main__":
    unittest.main()
