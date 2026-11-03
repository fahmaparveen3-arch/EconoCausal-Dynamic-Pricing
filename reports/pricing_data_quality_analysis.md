# Pricing Data Quality Analysis

## 1. Objective

The objective of this analysis is to assess the quality and consistency of the synthetic pricing dataset used in the EconoCausal project, *Dynamic Pricing via Double Machine Learning*.

Data quality is important because missing values, invalid discount rates, inconsistent prices, and incorrect purchase indicators can affect downstream analysis and pricing policy evaluation.

## 2. Dataset Overview

The synthetic pricing dataset contains 10,000 records and 14 columns.

The dataset includes customer characteristics, product information, discount assignment, purchase outcomes, and revenue-related fields.

| Category | Columns |
|---|---|
| Customer information | `customer_id`, `age`, `income`, `past_purchases` |
| Product information | `product_category`, `original_price` |
| Treatment information | `discount_rate`, `treatment` |
| Purchase outcomes | `purchase`, `units_sold`, `purchase_probability` |
| Financial information | `discounted_price`, `revenue`, `discount_cost` |

## 3. Data Quality Dimensions

### 3.1 Missing Values

Missing values should be checked across all columns before model training.

A missing value in a customer characteristic, discount field, or outcome variable may affect data preparation and model estimation.

**Validation approach:** Calculate the number and percentage of missing values in each column.

### 3.2 Duplicate Records

Duplicate records should be investigated to determine whether they represent repeated customer observations or accidental duplication.

The `customer_id` column can be checked for duplicates, but repeated customer IDs should only be treated as errors if the dataset design expects one record per customer.

**Validation approach:** Check duplicate rows and duplicate customer IDs separately.

### 3.3 Numeric Ranges

Numeric fields should be checked against their expected ranges.

- `age`: should follow the documented age range.
- `income`: should be non-negative.
- `past_purchases`: should be non-negative.
- `original_price`: should be positive.
- `discount_rate`: should be between 0 and 1.
- `purchase_probability`: should be between 0 and 1.
- `units_sold`: should be non-negative.
- `revenue` and `discount_cost`: should follow the project's financial calculation rules.

These checks should be aligned with the dataset-generation logic and project assumptions.

### 3.4 Discounted Price Consistency

The discounted price should agree with the original price and discount rate.

The expected relationship is:

`discounted_price = original_price × (1 − discount_rate)`

Small differences may arise from rounding to two decimal places.

Records that do not satisfy this relationship within an appropriate rounding tolerance should be investigated.

### 3.5 Treatment and Purchase Indicators

The `treatment` and `purchase` columns should contain valid binary values if the project defines them as binary indicators.

The treatment definition must also be documented clearly. A binary treatment indicator does not, by itself, identify the effect of every possible discount level.

### 3.6 Revenue and Discount Cost

Financial columns should be checked for consistency with the project's business rules.

For example, revenue may depend on the discounted price, units sold, and purchase outcome. Discount cost may depend on the discount amount and quantity sold.

The exact formulas must be confirmed from the dataset-generation code before these relationships are treated as validation rules.

## 4. Validation Methodology

The analysis follows these steps:

1. Load the synthetic pricing dataset.
2. Inspect its dimensions and column data types.
3. Calculate missing-value counts and percentages.
4. Check duplicate rows and customer IDs.
5. Validate numeric ranges and binary indicators.
6. Recalculate expected discounted prices and compare them with recorded values.
7. Investigate inconsistencies in purchase outcomes and financial fields.
8. Document findings and limitations before downstream modeling.

## 5. Validation Results

The existing dataset validation script was tested against the synthetic pricing dataset.

| Metric | Result |
|---|---|
| Number of records | 10,000 |
| Number of columns | 14 |
| Issues returned by the existing validator | 0 |
| Total unit tests | 10 |
| Passed tests | 10 |
| Failed tests | 0 |

### 5.1 Unit Test Coverage

The validation module is covered by the following ten unit tests:

1. Valid dataset produces no validation issues.
2. Missing required columns are reported.
3. Discount rates outside the valid range are reported.
4. Duplicate customer IDs are reported.
5. Inconsistent discounted prices are reported.
6. Empty datasets are reported.
7. Missing values in existing columns are reported.
8. Invalid treatment values are reported.
9. Invalid purchase values are reported.
10. Boundary discount rates of 0 and 1 are accepted.

### 5.2 Testing Outcome

All ten unit tests passed successfully using pytest.

The additional test cases improve coverage of missing values, binary treatment and purchase indicators, and boundary conditions for discount rates.

The zero-issue validation result applies to the dataset checks implemented in the validation function. It does not establish that every possible data-quality issue has been eliminated.

## 6. Limitations

The dataset is synthetic rather than directly observed retail transaction data. Therefore, its patterns and model results depend on the assumptions used to generate it.

Passing data-quality checks does not prove that the synthetic data accurately represents real customers,