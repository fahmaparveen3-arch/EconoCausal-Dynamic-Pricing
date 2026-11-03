# Pricing Calculation Validation Report

## 1. Objective

This report documents the validation of pricing calculations in the synthetic pricing dataset used in the EconoCausal Dynamic Pricing project.

The objective is to verify that discounted prices, revenue, and discount costs are calculated correctly and that purchase-related values remain consistent.

## 2. Validation Scope

The validation was implemented in:

`src/validate_pricing_calculations.py`

The script checks the required columns, validates numeric values, detects missing or non-finite values, and verifies pricing calculations.

## 3. Validation Checks

The following seven checks are performed:

1. **Discounted Price Calculation:** Verifies that the discounted price matches the original price after applying the discount rate.
2. **Revenue Calculation:** Checks revenue using the original price, discount rate, and units sold, with rounding applied to the final result.
3. **Discount Cost Calculation:** Verifies the total discount cost for the units sold.
4. **Purchase and Units Consistency:** Checks that customers with a purchase outcome have positive units sold and non-purchasers have zero units sold.
5. **Valid Purchase Values:** Ensures purchase values are either 0 or 1.
6. **Valid Discount Rates:** Ensures discount rates fall between 0 and 1.
7. **Non-negative Financial Values:** Checks that prices, quantities, revenue, and discount costs are non-negative.

## 4. Dataset Overview

The validation was previously performed on the synthetic pricing dataset, which contained:

- Total records: 10,000
- Total columns: 14
- Dataset path: `data/synthetic_pricing.csv`

## 5. Validation Results

The previous validation run reported:

- Total checks: 7
- Passed checks: 7
- Failed checks: 0
- Final result: PASS

All seven checks passed without mismatches in that run.

## 6. Important Calculation Detail

Revenue is calculated using the original price and discount rate before rounding the final revenue value.

The stored discounted price is rounded separately. Therefore, multiplying the stored rounded discounted price by units sold may produce small differences from the recorded revenue.

This distinction is important when validating financial calculations.

## 7. Limitations

The validation checks mathematical consistency and basic value constraints. It does not establish that the synthetic dataset represents real customer behaviour or that the pricing model will perform equally well in real-world conditions.

## 8. Conclusion

The pricing calculation validation script provides an additional layer of quality assurance for the synthetic pricing dataset.

The previous run passed all seven checks with zero mismatches, supporting the consistency of the tested pricing and financial calculations.


