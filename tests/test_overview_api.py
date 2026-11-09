
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

import src.api as api


class TestOverviewAPI(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_dir = Path(self.temp_dir.name)
        self.client = TestClient(api.app)

        self.dataset = self.data_dir / "synthetic_pricing.csv"
        self.dataset.write_text(
            "customer_id,treatment,purchase,discount_rate,revenue,discount_cost\n"
            "1,0,0,0.00,0,0\n"
            "2,0,0,0.00,0,0\n"
            "3,1,1,0.05,95,5\n"
            "4,1,0,0.20,0,0\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_overview_returns_metrics(self):
        with patch.object(api, "DATA_DIR", self.data_dir):
            response = self.client.get("/api/overview")

        self.assertEqual(response.status_code, 200)

        result = response.json()

        self.assertEqual(result["total_customers"], 4)
        self.assertEqual(result["data_type"], "synthetic")
        self.assertEqual(result["overall_purchase_rate_percent"], 25.0)

        baseline = result["purchase_baseline"]

        self.assertEqual(baseline["control_customers"], 2)
        self.assertEqual(baseline["treated_customers"], 2)
        self.assertEqual(baseline["control_purchase_rate_percent"], 0.0)
        self.assertEqual(baseline["treated_purchase_rate_percent"], 50.0)
        self.assertEqual(
            baseline["observed_difference_percentage_points"],
            50.0,
        )

        self.assertEqual(len(result["discount_analysis"]), 3)
        self.assertEqual(result["financial_totals"]["total_revenue"], 95.0)
        self.assertEqual(
            result["financial_totals"]["total_discount_cost"],
            5.0,
        )

    def test_overview_missing_dataset(self):
        with patch.object(api, "DATA_DIR", self.data_dir):
            self.dataset.unlink()
            response = self.client.get("/api/overview")

        self.assertEqual(response.status_code, 404)

    def test_overview_missing_required_column(self):
        self.dataset.write_text(
            "customer_id,treatment,purchase\n"
            "1,0,0\n"
            "2,1,1\n",
            encoding="utf-8",
        )

        with patch.object(api, "DATA_DIR", self.data_dir):
            response = self.client.get("/api/overview")

        self.assertEqual(response.status_code, 422)

    def test_overview_rejects_invalid_purchase_values(self):
        self.dataset.write_text(
            "customer_id,treatment,purchase,discount_rate,revenue,discount_cost\n"
            "1,0,2,0.00,0,0\n"
            "2,1,1,0.05,95,5\n",
            encoding="utf-8",
        )

        with patch.object(api, "DATA_DIR", self.data_dir):
            response = self.client.get("/api/overview")

        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
