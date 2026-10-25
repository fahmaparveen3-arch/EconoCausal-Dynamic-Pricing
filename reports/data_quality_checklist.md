# Data Quality Checklist

## 1. Objective

This checklist defines the data-quality checks required before using the pricing dataset for exploratory data analysis, causal inference, and profit evaluation.

## 2. Dataset Structure

The project uses a synthetic dataset representing 10,000 simulated customer records across five discount levels: 0%, 5%, 10%, 15%, and 20%.

The dataset should be checked to confirm that its structure matches the project's expected schema.

## 3. Required Quality Checks

### Missing Values
- Identify missing values in important columns.
- Determine whether missing values affect treatment assignment, customer outcomes, or profit calculations.
- Document any handling or removal of incomplete records.

### Duplicate Records
- Check for duplicate customer records.
- Determine whether repeated customer IDs are expected or indicate accidental duplication.

### Discount Values
- Verify that discount values belong to the expected set: 0%, 5%, 10%, 15%, and 20%.
- Flag negative discounts and values outside the permitted range.

### Outcome Validity
- Check that purchase outcomes use valid values, such as 0 and 1, if the project represents purchase as a binary variable.
- Confirm that revenue and profit values follow the definitions used in the project.

### Data Types
- Check that numerical variables use suitable numeric data types.
- Confirm that categorical variables are represented consistently.

### Logical Consistency
- Investigate negative revenue values or unexpected profit values.
- Check that discount assignments, purchase outcomes, and calculated metrics follow the project's documented assumptions.

## 4. Documentation

For each check, record:
- The check performed.
- The result.
- Any issues identified.
- The corrective action, if required.

Do not report a check as passed until it has actually been performed.

## 5. Conclusion

Data-quality checks help reduce errors in exploratory analysis, treatment-effect estimation, and profit evaluation. Completing and documenting these checks improves the transparency and reproducibility of the project.

Because the current dataset is synthetic, its quality and the realism of its simulated relationships must be evaluated separately.