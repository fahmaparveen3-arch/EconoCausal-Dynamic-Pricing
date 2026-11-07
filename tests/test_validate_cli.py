import unittest
from pathlib import Path
from unittest.mock import patch

from src.validate_cli import main


class TestValidationCLI(unittest.TestCase):

    @patch("src.validate_cli.validate_dataset", return_value=True)
    def test_successful_validation_returns_zero(self, mock_validator):
        result = main(["sample.csv"])

        self.assertEqual(result, 0)
        mock_validator.assert_called_once_with(Path("sample.csv"))

    @patch("src.validate_cli.validate_dataset", return_value=False)
    def test_failed_validation_returns_one(self, mock_validator):
        result = main(["missing.csv"])

        self.assertEqual(result, 1)
        mock_validator.assert_called_once_with(Path("missing.csv"))

    @patch("src.validate_cli.validate_dataset", return_value=True)
    def test_relative_dataset_path_is_supported(self, mock_validator):
        main(["data/sample.csv"])

        mock_validator.assert_called_once_with(
            Path("data/sample.csv")
        )


if __name__ == "__main__":
    unittest.main()
