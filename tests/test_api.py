import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

import src.api as api


class TestValidationAPI(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_dir = Path(self.temp_dir.name)

        self.dataset = self.data_dir / "test_dataset.csv"
        self.dataset.write_text("id,value\n1,100\n", encoding="utf-8")

        self.client = TestClient(api.app)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_health_endpoint(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "healthy")

    def test_dataset_validation_success(self):
        def mock_validator(path):
            print("Dataset validation completed.")
            return True

        with patch.object(api, "DATA_DIR", self.data_dir):
            with patch.object(
                api, "validate_dataset", side_effect=mock_validator
            ):
                response = self.client.get(
                    "/api/validation/dataset/test_dataset.csv"
                )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["completed"])
        self.assertIn(
            "Dataset validation completed.",
            response.json()["report"]
        )

    def test_pricing_validation_success(self):
        def mock_validator(path):
            print("Pricing checks passed.")
            return True

        with patch.object(api, "DATA_DIR", self.data_dir):
            with patch.object(
                api,
                "validate_pricing_calculations",
                side_effect=mock_validator
            ):
                response = self.client.get(
                    "/api/validation/pricing/test_dataset.csv"
                )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["passed"])
        self.assertIn(
            "Pricing checks passed.",
            response.json()["report"]
        )

    def test_missing_dataset(self):
        with patch.object(api, "DATA_DIR", self.data_dir):
            response = self.client.get(
                "/api/validation/dataset/missing.csv"
            )

        self.assertEqual(response.status_code, 404)

    def test_invalid_file_extension(self):
        with patch.object(api, "DATA_DIR", self.data_dir):
            response = self.client.get(
                "/api/validation/dataset/test.txt"
            )

        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
