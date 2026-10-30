# Dataset Validation Guide

## 1. Overview

This guide explains how to validate the synthetic pricing dataset used in the EconoCausal Dynamic Pricing project.

The validation script checks basic dataset quality, discount values, treatment consistency, purchase outcomes, and customer identifiers before further analysis.

**Script:** `src/validate_data.py`  
**Dataset:** `data/synthetic_pricing.csv`

## 2. Prerequisites

Before running the script, ensure that:

- Python is installed.
- Pandas is installed.
- The project repository is available locally.
- The dataset CSV file exists at the expected path.

Install Pandas if needed:

```bash
python -m pip install pandas
```

## 3. Running the Validation Script

Open a terminal in the project root directory and run:

```bash
python src/validate_data.py
```

When prompted, enter the dataset path:

```text
data/synthetic_pricing.csv
```

If the dataset path contains spaces, enter the path in quotation marks.

## 4. Validation Checks

The script performs the following checks:

| Check | Purpose |
|---|---|
| Dataset structure | Reports the number of rows and columns. |
| Missing values | Counts missing values across the dataset and by column. |
| Duplicate rows | Identifies rows that are exact duplicates. |
| Column data types | Displays the inferred data type of each column. |
| Discount validation | Checks recognised discount columns against the allowed discount levels. |
| Treatment consistency | Checks that treatment is binary and consistent with whether the discount is greater than zero. |
| Purchase outcome | Checks that purchase values are binary. |
| Customer identifiers | Reports unique, missing, and duplicate customer IDs. |

The project uses the discount levels 0%, 5%, 10%, 15%, and 20%. In `discount_rate`, these are represented as 0.00, 0.05, 0.10, 0.15, and 0.20.

## 5. Recorded Validation Results

The initial validation run on `data/synthetic_pricing.csv` reported:

- Rows: 10,000
- Columns: 14
- Duplicate rows: 0
- Missing values: 0
- Invalid discount values: 0
- Invalid treatment values: 0
- Treatment-discount inconsistencies: 0
- Invalid purchase values: 0
- Unique customer IDs: 10,000
- Missing customer IDs: 0
- Duplicate customer IDs: 0

These results describe the recorded validation run. Rerun the script whenever the dataset changes.

## 6. Understanding the Output

A validation report with no detected issues indicates that the checks implemented in the script did not find the corresponding data-quality problems.

If the script reports an issue:

1. Identify the affected column or validation check.
2. Inspect the relevant dataset records.
3. Determine whether the issue is caused by incorrect data or an incorrect validation assumption.
4. Correct the underlying problem where appropriate.
5. Rerun the validation script and review the new output.

Do not modify the data solely to make a validation check pass without understanding the cause.

## 7. Limitations

This script provides basic data-quality checks. It does not establish that:

- The dataset represents real customer behaviour.
- The DML model is correctly implemented or accurately estimates treatment effects.
- The assumptions required for causal inference hold.
- The pricing policy will produce the same results in a real business setting.

The dataset is synthetic, and model-level evaluation must be conducted separately before drawing conclusions about causal effects or pricing effectiveness.

## 8. Reproducibility

To reproduce the recorded checks:

1. Use the project repository and the intended dataset version.
2. Ensure Python and Pandas are available.
3. Run `python src/validate_data.py` from the project root.
4. Enter `data/synthetic_pricing.csv` when prompted.
5. Review the complete validation output.
6. Record any differences from the results documented in this guide.

For consistent comparisons, use the same dataset version and document any changes to the validation script or its assumptions.