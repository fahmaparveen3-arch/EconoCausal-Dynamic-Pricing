# EconoCausal – Final Project Progress Update & Handover Report

**Date:** 10 November 2026
**Project:** EconoCausal – Dynamic Pricing via Double Machine Learning
**Internship Role:** Data Associate L1 Intern
**Branch:** Afnan
**Integrated Team Branch:** Hiba

## 1. Project Overview

EconoCausal focuses on estimating the causal impact of marketing campaigns and pricing interventions using causal machine learning, particularly Double Machine Learning (DML).

The project explores treatment-effect estimation, uplift modelling, pricing policy evaluation, and dynamic pricing under controlled experimental assumptions.

## 2. Backend and Analytical Progress

The backend and analytical work completed within the reviewed project scope includes:

- Data collection, loading, cleaning, and exploratory data analysis.
- Hillstrom email campaign treatment-effect and uplift analysis.
- LinearDML and T-learner modelling.
- Discount treatment-effect analysis and dynamic pricing policy comparison.
- Model evaluation, validation, and robustness analysis.
- Pricing data validation and business-rule checks.
- Automated tests, technical documentation, and analytical reports.

## 3. Datasets

Three datasets were used for different analytical purposes.

### 3.1 Hillstrom Email Marketing Dataset

- Contains 64,000 records covering Men's Email, Women's Email, and No Email groups.
- Used for marketing treatment-effect estimation and uplift analysis.
- Represents an email marketing experiment, not a randomized pricing experiment.

### 3.2 UCI Online Retail Dataset

- Observational transaction data.
- Used to explore price, sales, and revenue patterns.
- Does not provide randomized pricing experiments and has limitations for causal inference.

### 3.3 Synthetic Pricing Dataset

- Contains 10,000 records and 14 columns.
- Used to test pricing methods under controlled assumptions.
- Supports experimentation with treatment, discount, purchase, revenue, and pricing variables.

## 4. Key Analytical Results

### 4.1 Hillstrom Campaign Analysis

- No Email conversion rate: 0.573%.
- Men's Email conversion rate: 1.253%.
- Women's Email conversion rate: 0.884%.
- Men's Email treatment effect versus No Email: approximately +0.681 percentage points.
- Women's Email treatment effect versus No Email: approximately +0.311 percentage points.
- Top 20% observed uplift:
  - Random Forest T-learner: 1.311 percentage points.
  - HistGradientBoosting T-learner: 1.305 percentage points.

### 4.2 Predictive Model Evaluation

- Baseline conversion model ROC-AUC: 0.5490.
- Baseline conversion model PR-AUC: 0.0103.

These results indicate limited predictive performance from the baseline conversion model.

### 4.3 Synthetic Dynamic Pricing Experiment

Expected profit per customer under the tested discount policies:

| Discount Policy | Expected Profit |
|---|---:|
| 0% discount | 33.24 |
| 5% discount | 33.42 |
| 10% discount | 32.85 |
| 15% discount | 31.41 |
| 20% discount | 28.93 |

The 5% discount produced the highest expected profit among the tested synthetic policies.

This result depends on the assumptions of the synthetic experiment and should not be interpreted as a real-world pricing guarantee.

### 4.4 LinearDML Evaluation

| Metric | Full Data | Holdout |
|---|---:|---:|
| True ATE | 0.074463 | 0.074861 |
| Estimated ATE | 0.079521 | 0.092794 |
| MAE | 0.016636 | 0.020994 |
| RMSE | 0.020166 | 0.024203 |

The holdout estimate showed greater deviation from the true ATE than the full-data estimate.

### 4.5 Online Retail Analysis

- Estimated price coefficient: 0.3691.
- p-value: 0.7658.
- The estimated coefficient was not statistically significant.

Since the dataset is observational, this result cannot independently establish a causal price effect.

## 5. Data Validation and Testing

### 5.1 Pricing Data Validation

The Afnan branch includes a reusable pricing data validation module:

`src/data_processing/validate_pricing_data.py`

The validation checks include:

- Required columns and missing values.
- Duplicate customer IDs.
- Numeric data types and valid values.
- Discount-rate boundaries.
- Treatment and purchase values.
- Discounted-price calculations.
- Revenue calculations.
- Discount-cost calculations.
- Purchase probability boundaries.
- Nonnegative pricing and sales values.

### 5.2 Business-Logic Validation Contribution

On 9 November 2026, additional business-rule validation was implemented.

The validation checks:

1. Revenue consistency:

   `revenue = discounted_price × units_sold`

2. Discount-cost consistency:

   `discount_cost = (original_price - discounted_price) × units_sold`

Two additional automated tests were added:

- `test_inconsistent_revenue_is_reported`
- `test_inconsistent_discount_cost_is_reported`

The complete Afnan branch test run reported 15 passing tests.

### 5.3 Broader Project Testing

The team previously reported 38 passing tests across the broader project test suite, covering areas such as preprocessing, pricing calculations, DML evaluation, and pipeline checks.

The 38-test result and the 15-test Afnan validation result represent different test scopes and should not be combined.

## 6. Team Integration and Application Development

The integrated team branch `Hiba` contains the broader application implementation.

The latest reviewed integration commit is:

- Commit: `6708316`
- Message: `Integrate FastAPI backend with dynamic pricing dashboard`
- Branch: `origin/Hiba`

The commit changed the following files:

| File | Change |
|---|---|
| `backend/main.py` | 666 lines added |
| `frontend/src/app/page.tsx` | 332 additions and 70 deletions |
| `requirements.txt` | 3 additions |

The integrated project includes a FastAPI backend and a frontend dynamic pricing dashboard.

This section records the state of the integrated team branch and does not imply that all application integration work was individually implemented on the Afnan branch.

## 7. Documentation and Individual Contributions

The following documentation and validation contributions are recorded on the Afnan branch:

- Causal problem understanding.
- Dataset research and selection.
- Causal DAG documentation.
- Double Machine Learning methodology documentation.
- Pricing data validation guide.
- Pricing validation test cases.
- Model evaluation and business insights documentation.
- Project integration review.
- Day 20 business-logic validation and automated tests.
- Day 21 integration audit report.

### Day 20 – Business-Logic Validation

Implemented revenue and discount-cost consistency checks and added two automated tests.

Commit: `6307227`
Message: `feat: validate revenue and discount cost calculations`

### Day 21 – Integration Audit

Reviewed the Afnan branch against the integrated Hiba branch, including differences in source modules, tests, documentation, validation logic, and application structure.

Created:

`docs/integration_audit_2026-11-10.md`

Commit: `d070ea1`
Message: `docs: add Day 21 integration audit report`

The Day 21 audit commit was successfully pushed to `origin/Afnan`.

## 8. Current Limitations

- Synthetic pricing results depend on the assumptions used to generate the data.
- Hillstrom is a marketing experiment, not a randomized pricing experiment.
- Online Retail data is observational and has limitations for causal inference.
- The baseline conversion model has limited predictive performance.
- Synthetic DML results do not guarantee performance on real-world data.
- Production deployment and final end-to-end verification have not been confirmed in this review.
- Further integration and deployment validation may be required.

## 9. Final Project Handover Status

The project has progressed through data preparation, exploratory analysis, causal modelling, dynamic pricing evaluation, validation, and application development.

The integrated team branch contains the FastAPI backend and dynamic pricing dashboard integration changes.

The following items should be verified before considering the application fully deployment-ready:

1. Complete end-to-end frontend and backend testing.
2. Verify API and dashboard connectivity.
3. Validate application behaviour using appropriate test data.
4. Complete production configuration and deployment.
5. Verify the final deployed application.

## 10. Overall Conclusion

EconoCausal demonstrates the application of causal machine learning techniques to marketing treatment-effect analysis and dynamic pricing experimentation.

The project includes multiple dataset analyses, DML and uplift modelling, synthetic pricing policy evaluation, reusable data validation, automated tests, documentation, and a team-integrated application foundation.

The Afnan branch contains individual documentation and pricing validation contributions, while the Hiba branch contains the latest reviewed integrated application changes.

This report serves as the final progress summary and handover record for the reviewed project work as of 10 November 2026.
