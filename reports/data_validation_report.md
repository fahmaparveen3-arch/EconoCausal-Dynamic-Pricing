# Data Validation Report

## 1. Objective

This report documents the initial data-quality checks performed on the synthetic pricing dataset used in the EconoCausal Dynamic Pricing project.

## 2. Dataset Overview

The dataset was loaded from:

`data/synthetic_pricing.csv`

The initial validation run reported:

- Total records: 10,000
- Total columns: 14
- Duplicate rows: 0
- Missing values: 0

## 3. Variables Identified

The dataset includes variables related to:

- Customer information: `customer_id`, `age`, `income`
- Purchase history: `past_purchases`
- Product information: `product_category`, `original_price`
- Discount assignment: `discount_rate`, `treatment`
- Customer outcome: `purchase`, `units_sold`
- Financial measures: `discounted_price`, `revenue`, `discount_cost`
- Model-related information: `purchase_probability`

## 4. Initial Findings

The initial run found no missing values or duplicate rows.

The dataset contains customer, discount, purchase, and financial variables that can support further exploratory analysis and pricing evaluation.

These checks describe basic data quality. They do not establish that the simulated data accurately represents real customer behaviour.

## 5. Additional Checks

The validation script was extended to check:

- Whether discount values match the expected levels.
- Whether purchase outcomes contain only valid binary values.
- Whether customer identifiers are missing.
- The dataset's column data types.

The results of these additional checks should be recorded after running the updated validation script.

## 6. Limitations

The dataset is synthetic. Passing basic data-quality checks does not establish causal validity, model accuracy, or real-world applicability.

Further validation is required before making pricing recommendations.

## 7. Conclusion

The initial validation run confirmed that the dataset contains 10,000 rows and 14 columns, with no missing values or duplicate rows detected.

Additional checks can help identify invalid discount assignments and purchase outcomes before the dataset is used for further analysis.