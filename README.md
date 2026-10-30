# EconoCausal — Dynamic Pricing

## 1. Project Overview

EconoCausal is a data science project exploring causal inference, uplift modelling, customer behaviour, and data-driven pricing decisions.

The project combines three complementary analytical components:

1. **Hillstrom Randomized Marketing Experiment:** Studies the causal effects of email marketing campaigns and customer-level uplift.
2. **UCI Online Retail Dataset:** Examines historical product sales, transaction prices, and demand patterns using real-world observational data.
3. **Synthetic Discount-Pricing Experiment:** Uses simulated customer data and Double Machine Learning (DML) to estimate treatment effects, validate models against known reference effects, and compare pricing policies.

The project uses Python, statistical analysis, machine learning, causal inference, and automated testing to investigate how customer behaviour can inform business decisions.

**Important distinction:** These datasets serve different purposes. Hillstrom supports randomized marketing analysis, Online Retail supports observational product-demand analysis, and synthetic data supports controlled pricing simulations. Results from one component do not independently validate the others.

## 2. Project Objectives

- Analyze treatment effects in a randomized marketing experiment.
- Explore customer-level treatment-effect estimation using machine learning.
- Examine product sales and historical price variations using real transaction data.
- Identify relationships between selling prices and product demand.
- Generate and validate synthetic customer-pricing data.
- Evaluate DML estimates against known synthetic reference effects.
- Compare causal estimators using repeated train/test splits.
- Compare candidate pricing policies using expected purchase rates, revenue, and profit.
- Build reusable Python modules, automated tests, and evaluation reports.
- Document assumptions, estimation errors, and limitations transparently.

## 3. Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| Data analysis | pandas, NumPy |
| Machine learning | scikit-learn |
| Causal inference | EconML, Double Machine Learning |
| Statistical analysis | SciPy, statsmodels |
| Visualization | Matplotlib, Seaborn |
| Data storage | CSV, Excel |
| Testing | pytest |
| Version control | Git, GitHub |
| Development environment | Jupyter Notebook, VS Code |

## 4. Project Structure

The following structure represents the main project components. Local datasets and generated files are stored separately.

```text
EconoCausal-Dynamic-Pricing/
│
├── data/
│   ├── hillstrom.csv
│   ├── synthetic_pricing.csv
│   ├── prepared_pricing.csv
│   ├── online+retail/
│   │   └── Online Retail.xlsx
│   └── processed/
│       ├── online_retail_cleaned.csv
│       ├── online_retail_excluded.csv
│       ├── online_retail_fully_reversed_audit.csv
│       ├── online_retail_non_product_audit.csv
│       ├── online_retail_product_sales.csv
│       └── online_retail_returns_cancellations.csv
│
├── notebooks/
│   ├── 01_hillstrom_eda.ipynb
│   ├── 01_hillstrom_eda_backup.ipynb
│   ├── 02_online_retail_eda.ipynb
│   └── 02_online_retail_eda_recovered.ipynb
│
├── src/
│   ├── data_processing/
│   │   ├── clean_data.py
│   │   ├── generate_synthetic_pricing_data.py
│   │   ├── load_data.py
│   │   ├── load_pricing_data.py
│   │   ├── prepare_pricing_data.py
│   │   └── preprocess_online_retail.py
│   │
│   ├── models/
│   │   ├── train_dml.py
│   │   └── train_uplift.py
│   │
│   ├── evaluation/
│   │   ├── compare_dml_estimators.py
│   │   ├── compare_pricing_policies.py
│   │   ├── evaluate_pricing_profit.py
│   │   ├── evaluate_uplift.py
│   │   ├── validate_dml_against_truth.py
│   │   └── validate_dml_holdout.py
│   │
│   └── pricing/
│       └── dynamic_pricing.py
│
├── reports/
│   ├── dml_customer_effects.csv
│   ├── dml_estimator_comparison.csv
│   ├── dml_estimator_repeated_seed_summary.csv
│   ├── dml_holdout_validation.csv
│   ├── dml_truth_validation.csv
│   ├── pricing_policy_comparison.csv
│   └── pricing_profit_evaluation.csv
│
├── tests/
│   ├── test_dynamic_pricing.py
│   └── test_train_dml.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

The recovered Online Retail notebook is retained as a backup. The main analysis notebook is `02_online_retail_eda.ipynb`.

## 5. Datasets

### 5.1 Hillstrom Randomized Marketing Dataset

The Hillstrom dataset contains 64,000 customer records from a randomized email-marketing experiment.

It includes:

- Customer characteristics.
- Marketing treatment groups.
- Visit information.
- Conversion outcomes.
- Customer spending.

The analysis compares men's email and women's email campaigns against a no-email control group.

Previously recorded results:

| Analysis | Result |
|---|---:|
| Men's email vs. no email: conversion difference | +0.681 percentage points |
| Women's email vs. no email: conversion difference | +0.311 percentage points |
| Uplift model ROC-AUC | 0.5490 |
| Uplift model PR-AUC | 0.0103 |
| Mean predicted uplift | 0.632 percentage points |

These results should be reproduced from the relevant notebook or scripts before final submission.

### 5.2 Synthetic Discount-Pricing Dataset

The synthetic pricing dataset contains 10,000 customer records generated using a predefined simulation process.

It represents:

- Customer characteristics.
- Product categories.
- Discount assignments.
- Purchase outcomes.
- Generated purchase probabilities.

The dataset supports experiments involving:

- Discount assignment.
- Causal-effect estimation.
- Customer-level treatment-effect prediction.
- Synthetic ground-truth validation.
- Pricing-policy comparison.

Because the data are synthetic, the results demonstrate model behaviour under specified simulation assumptions rather than proven real-world business performance.

### 5.3 UCI Online Retail Dataset

The Online Retail dataset was obtained from the UCI Machine Learning Repository.

It contains historical transactions from a UK-based online retailer between December 2010 and December 2011.

Original dataset characteristics:

| Description | Value |
|---|---:|
| Original records | 541,909 |
| Original columns | 8 |
| Data format | Excel |
| Data period | December 2010 – December 2011 |

The dataset contains transaction information such as:

- Invoice number.
- Product stock code.
- Product description.
- Quantity purchased.
- Invoice date.
- Unit price.
- Customer ID.
- Country.

**Dataset source:** [UCI Machine Learning Repository — Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail)

**License:** Creative Commons Attribution 4.0 International (CC BY 4.0).

The dataset is observational. It records historical transactions rather than randomized price assignments. Therefore, its price-demand analysis is exploratory and does not establish causal price elasticity.

## 6. Data Preprocessing

### 6.1 Hillstrom Data Preparation

The Hillstrom workflow includes:

- Loading the randomized marketing dataset.
- Checking required columns.
- Examining missing values.
- Comparing treatment and control groups.
- Preparing customer characteristics for modelling.
- Separating treatment assignments and outcomes.

### 6.2 Synthetic Pricing Data Preparation

The synthetic pricing workflow includes:

- Generating customer records using a fixed random seed.
- Preparing treatment and outcome variables.
- Validating required columns and numeric values.
- Selecting customer characteristics as model features.
- Excluding generated purchase probabilities from DML features to avoid target leakage.

### 6.3 Online Retail Data Preprocessing

The Online Retail preprocessing workflow is implemented in:

`src/data_processing/preprocess_online_retail.py`

The preprocessing process includes:

1. Loading the original Excel dataset.
2. Checking and removing exact duplicate records.
3. Converting invoice dates and numeric columns into appropriate data types.
4. Separating cancellation records.
5. Identifying fully reversed sales groups using matching customer, product, price, date, and quantity information.
6. Separating return records.
7. Excluding invalid sales records.
8. Handling missing product descriptions.
9. Calculating transaction revenue.
10. Separating merchandise sales from non-product charges.
11. Exporting cleaned datasets and audit files.

Preprocessing summary:

| Processing stage | Records |
|---|---:|
| Original dataset | 541,909 |
| After duplicate removal | 536,641 |
| Cancellation records | 9,251 |
| Fully reversed audit records | 1,206 |
| Fully reversed original sales removed | 603 |
| Return records | 1,336 |
| Invalid sales excluded | 1,176 |
| Clean sales | 524,275 |
| Product sales | 521,917 |
| Non-product records separated | 2,358 |

The product-level analysis uses 521,917 merchandise transaction records.

The following output files are generated:

| File | Purpose |
|---|---|
| `online_retail_cleaned.csv` | Cleaned sales data |
| `online_retail_excluded.csv` | Excluded records |
| `online_retail_fully_reversed_audit.csv` | Audit of fully reversed sales groups |
| `online_retail_non_product_audit.csv` | Separated non-product charges |
| `online_retail_product_sales.csv` | Merchandise-only transaction data |
| `online_retail_returns_cancellations.csv` | Return and cancellation records |

Non-product charges such as postage, manual charges, carriage, bank charges, and other service fees are separated from merchandise sales and retained in the audit outputs.

Valid merchandise transactions, including unusual bulk quantities and high-priced products, are not automatically removed merely because they are outliers.

### 6.4 Data Quality Validation

The cleaned product dataset was checked for:

- Duplicate records.
- Missing values.
- Invalid quantities.
- Invalid unit prices.
- Revenue calculation errors.
- Date consistency.

Validation results:

| Validation check | Result |
|---|---:|
| Product sales records | 521,917 |
| Duplicate rows | 0 |
| Missing product descriptions | 0 |
| Invalid quantities (≤ 0) | 0 |
| Invalid unit prices (≤ 0) | 0 |
| Revenue calculation discrepancies | 0 |

CustomerID is missing in approximately 25.2% of cleaned product sales records.

These records are retained for product-level analysis but should be excluded from customer-level analysis when a customer identifier is required.

## 7. Methodology

### 7.1 Randomized Marketing Causal Analysis

The Hillstrom analysis compares marketing treatment groups with the no-email control group.

The main comparison estimates the difference in conversion rates between customers receiving men's email marketing and customers receiving no email.

Customer characteristics are used for uplift modelling to investigate variation in treatment effects.

### 7.2 Double Machine Learning

The synthetic pricing implementation uses EconML's `LinearDML`, random-forest nuisance models, and one-hot encoding for categorical features.

The pricing model represents discount assignment as a binary treatment and estimates customer-level treatment effects relative to a control condition.

**Limitation:** The binary treatment combines multiple discount levels. It does not independently identify the causal effect of each specific discount percentage.

### 7.3 Synthetic Ground-Truth Validation

Because the synthetic pricing data are generated using a known simulation process, reference treatment effects can be calculated from the underlying purchase-probability formula.

The validation workflow compares estimated effects with synthetic reference effects using:

- Average Treatment Effect (ATE).
- ATE estimation bias.
- Individual-effect Mean Absolute Error (MAE).
- Individual-effect Root Mean Squared Error (RMSE).

These metrics quantify estimation error under the specified simulation. They do not establish real-world causal validity.

### 7.4 Holdout Evaluation

The holdout evaluation separates customers into training and test partitions.

Models are fitted using training data and evaluated on unseen test customers.

Comparing estimated treatment effects with synthetic reference effects provides an out-of-sample diagnostic.

### 7.5 Repeated-Seed Estimator Comparison

The estimator-comparison workflow evaluates LinearDML and NonParamDML using five random seeds:

`42, 7, 21, 35, 99`

For each seed, both estimators use the same stratified train/test split.

The evaluation includes:

- True and estimated ATE.
- ATE bias.
- Individual-effect MAE and RMSE.
- Correlation between estimated and reference individual effects.
- Mean and standard deviation across repeated runs.

Repeated-seed evaluation helps assess sensitivity to data partitioning. It is not equivalent to evaluation on independent real-world datasets.

### 7.6 Online Retail Product-Demand Analysis

The Online Retail analysis is conducted in:

`notebooks/02_online_retail_eda.ipynb`

The cleaned merchandise dataset is used to investigate product-level transaction patterns and historical selling-price variation.

The analysis includes:

- Product and invoice counts.
- Revenue distribution.
- Monthly revenue trends.
- Product-level sales performance.
- Price distribution.
- Selection of frequently purchased products.
- Monthly quantity and weighted-average selling-price analysis.
- Exploratory price-quantity correlation.
- Pooled regression with product and month fixed effects.

Five frequently purchased products were selected for detailed monthly analysis:

| Stock Code | Product |
|---|---|
| 85123A | White Hanging Heart T-Light Holder |
| 85099B | Jumbo Bag Red Retrospot |
| 22423 | Regency Cake Stand 3 Tier |
| 47566 | Party Bunting |
| 20725 | Lunch Bag Red Retrospot |

The monthly analysis uses StockCode as the product identifier to handle occasional variations in product descriptions.

Monthly quantity sold and weighted-average selling prices are examined across the available observation period.

### 7.7 Exploratory Price-Demand Findings

The monthly price-quantity correlations for the five selected products were:

| Product | Correlation | p-value |
|---|---:|---:|
| Lunch Bag Red Retrospot | -0.3388 | 0.2575 |
| Regency Cake Stand 3 Tier | +0.1984 | 0.5158 |
| Party Bunting | -0.0916 | 0.7660 |
| Jumbo Bag Red Retrospot | +0.1192 | 0.6982 |
| White Hanging Heart T-Light Holder | +0.0815 | 0.7911 |

None of the five correlations was statistically significant at the 5% level.

A pooled regression using log quantity, log weighted-average price, product fixed effects, and month fixed effects produced:

| Metric | Result |
|---|---:|
| Price coefficient | +0.3416 |
| Standard error | 1.2339 |
| t-statistic | 0.2769 |
| p-value | 0.7831 |
| Observations | 65 |
| Degrees of freedom | 47 |

The analysis did not identify a statistically reliable price-quantity association in the selected monthly observations.

This does not prove that price has no effect on demand. The analysis is limited by the observational nature of the data, the small number of products and monthly observations, and potential confounding factors such as seasonality, promotions, and customer composition.

The results should not be interpreted as causal price elasticity.

### 7.8 Pricing-Policy Comparison

The synthetic pricing-policy comparison evaluates five candidate discount levels:

- 0%
- 5%
- 10%
- 15%
- 20%

The same synthetic customer population is used for all candidate policies.

The report includes expected purchase rate, expected revenue per customer, expected profit per customer, and total expected profit.

## 8. Setup and Installation

Run commands from the project root in Windows PowerShell.

### 8.1 Activate the Existing Environment

The project currently uses a Python 3.13 virtual environment named `.venv313`.

```powershell
.\.venv313\Scripts\Activate.ps1
```

Alternatively, invoke the environment's Python executable directly:

```powershell
.\.venv313\Scripts\python.exe
```

### 8.2 Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

The required dependencies are listed in `requirements.txt`.

For reproducibility, dependency versions should be verified and documented before final submission.

## 9. Running the Project

Run the relevant scripts from the project root.

### 9.1 Generate Synthetic Pricing Data

```powershell
python src/data_processing/generate_synthetic_pricing_data.py
```

### 9.2 Prepare the Pricing Dataset

```powershell
python src/data_processing/prepare_pricing_data.py
```

### 9.3 Train the DML Model

```powershell
python src/models/train_dml.py
```

Output:

`reports/dml_customer_effects.csv`

### 9.4 Evaluate Pricing Profit

```powershell
python src/evaluation/evaluate_pricing_profit.py
```

Output:

`reports/pricing_profit_evaluation.csv`

### 9.5 Compare Pricing Policies

```powershell
python src/evaluation/compare_pricing_policies.py
```

Output:

`reports/pricing_policy_comparison.csv`

### 9.6 Validate Against Synthetic Ground Truth

```powershell
python -m src.evaluation.validate_dml_against_truth
```

Output:

`reports/dml_truth_validation.csv`

### 9.7 Evaluate DML on Holdout Customers

```powershell
python -m src.evaluation.validate_dml_holdout
```

Output:

`reports/dml_holdout_validation.csv`

### 9.8 Compare DML Estimators Across Repeated Seeds

```powershell
python src/evaluation/compare_dml_estimators.py
```

Output:

`reports/dml_estimator_repeated_seed_summary.csv`

The single-split estimator comparison report contains previously generated results and is not regenerated by the current repeated-seed script.

### 9.9 Preprocess Online Retail Data

Ensure that the original UCI Excel dataset is available at:

`data/online+retail/Online Retail.xlsx`

Then run:

```powershell
python src/data_processing/preprocess_online_retail.py
```

The cleaned datasets and audit files are generated in:

`data/processed/`

### 9.10 Explore Online Retail Data

Open the notebook:

`notebooks/02_online_retail_eda.ipynb`

Select the project's `.venv313` Python kernel and run the notebook cells.

The notebook contains the product-level exploratory analysis and price-demand investigation.

### 9.11 Run Automated Tests

```powershell
python -m pytest -v
```

The last recorded test result for the existing DML and pricing test files was 26 passing tests. The complete test suite should be rerun before final submission.

## 10. Pricing-Policy Results

The following results were previously recorded from the synthetic pricing-policy comparison.

| Discount | Expected purchase rate | Expected profit per customer | Total expected profit |
|---:|---:|---:|---:|
| 0% | 20.78% | 33.24 | 332,435.25 |
| 5% | 23.54% | 33.42 | 334,186.01 |
| 10% | 26.53% | 32.85 | 328,546.76 |
| 15% | 29.72% | 31.41 | 314,052.64 |
| 20% | 33.11% | 28.93 | 289,266.88 |

Under the current simulation assumptions, the **5% discount policy** produces the highest expected profit among the five tested policies.

Its total expected profit is 334,186.01 compared with 332,435.25 for the no-discount policy, representing an estimated improvement of approximately 0.53%.

The simulation illustrates a trade-off: larger discounts increase estimated purchase rates, but the reduction in selling price can outweigh the benefit of additional purchases.

### Assumptions

- The same synthetic customer records are used to evaluate all candidate policies.
- Expected units per purchase are assumed to be 1.15.
- Product-cost ratios are illustrative assumptions.
- Operating expenses and other business costs are excluded.
- Expected profit depends on the synthetic purchase-probability formula and its assumptions.

These results do not establish that 5% is the optimal discount for a real business.

## 11. DML Validation Results

The following are previously recorded synthetic validation results. They should be regenerated and verified before final submission.

### 11.1 Full-Dataset Synthetic Ground-Truth Validation

| Metric | Result |
|---|---:|
| Customers evaluated | 10,000 |
| True synthetic policy ATE | 0.074463 |
| Estimated DML ATE | 0.079521 |
| ATE estimation bias | 0.005058 |
| Individual-effect MAE | 0.016636 |
| Individual-effect RMSE | 0.020166 |

The estimated average effect exceeds the synthetic reference effect.

### 11.2 Holdout Validation

| Metric | Result |
|---|---:|
| Holdout customers evaluated | 2,500 |
| True synthetic policy ATE | 0.074861 |
| Estimated DML ATE | 0.092794 |
| ATE estimation bias | 0.017932 |
| Individual-effect MAE | 0.020994 |
| Individual-effect RMSE | 0.024203 |

The estimated holdout ATE is approximately 1.79 percentage points higher than the synthetic reference effect.

These results demonstrate estimation error and should not be presented as evidence of real-world pricing performance.

### 11.3 Repeated-Seed Estimator Comparison

The following summary was recorded from five evaluation runs, with 2,500 holdout customers per run.

| Metric | LinearDML | NonParamDML |
|---|---:|---:|
| Mean estimated ATE | 0.078459 | 0.078441 |
| Standard deviation of estimated ATE | 0.008678 | 0.007982 |
| Mean ATE bias | 0.003956 | 0.003938 |
| ATE-bias standard deviation | 0.008500 | 0.007810 |
| Mean MAE | 0.018963 | 0.035780 |
| Mean RMSE | 0.023124 | 0.050144 |
| Mean effect correlation | 0.617833 | 0.231091 |

In this experiment, LinearDML has lower mean MAE and RMSE and higher mean correlation with synthetic reference effects than NonParamDML.

The results support choosing LinearDML as the stronger candidate for further investigation under this particular simulation. They do not establish universal superiority.

## 12. Automated Tests

The existing test files cover areas including:

- Discounted-price calculations.
- Zero and full discounts.
- Invalid prices and discount values.
- Purchase-probability estimation.
- Expected-profit calculations.
- Candidate-discount comparisons.
- DML input validation.
- Missing columns and duplicate customer identifiers.
- Invalid treatment values.
- Handling of invalid numeric values.
- DML model fitting.
- Finite customer-level estimates.
- Holdout evaluation.

The last recorded test run reported 26 passing tests across the existing pricing and DML test files.

The full test suite should be rerun before final submission.

Passing tests confirms selected software behaviours; it does not by itself establish causal correctness or production readiness.

## 13. Limitations and Critical Analysis

### 13.1 Synthetic Data

The pricing dataset is simulated using predefined assumptions. Results may not generalize to real customers or markets.

**Mitigation:** Evaluate alternative data-generating scenarios and document the assumptions behind each experiment.

### 13.2 Binary Treatment Representation

The current DML model estimates a binary discount-versus-control effect even though the policy comparison contains five discount levels.

**Mitigation:** Investigate multi-treatment causal estimation or appropriately defined discount-versus-control comparisons.

### 13.3 Treatment-Effect Estimation Error

The recorded holdout estimate overstates the synthetic reference ATE by approximately 1.79 percentage points.

**Mitigation:** Verify the target estimand, compare suitable estimators, and evaluate stability across repeated holdout splits.

### 13.4 Observational Online Retail Data

Historical transaction data do not provide randomized price assignments. Observed price and quantity relationships may be influenced by seasonality, promotions, product differences, and customer composition.

**Mitigation:** Treat the current results as exploratory. Stronger causal price analysis requires suitable identification assumptions and, ideally, experimental or quasi-experimental evidence.

### 13.5 Limited Product-Level Analysis

The detailed Online Retail analysis focuses on five selected products and 13 monthly observations per product. December 2011 is incomplete because the dataset ends on December 9.

**Mitigation:** Extend analysis to more products and investigate appropriate time-based modelling when justified.

### 13.6 Missing Customer Identifiers

A substantial proportion of Online Retail records have missing CustomerID values.

**Mitigation:** Retain such records for product-level analysis but exclude them from analyses requiring reliable customer identification.

### 13.7 Simplified Profit Assumptions

Product costs are illustrative, and the synthetic simulation excludes shipping, marketing, taxes, returns, inventory costs, and operating expenses.

**Mitigation:** Make cost assumptions configurable and conduct sensitivity analysis.

### 13.8 Separate Marketing and Pricing Experiments

The Hillstrom email experiment does not directly measure discount effects.

**Mitigation:** Keep marketing uplift and pricing evaluation separate, connecting their methods only where the causal assumptions support it.

### 13.9 No Real-World Pricing Validation

The project does not yet demonstrate that its pricing recommendations improve actual business outcomes.

**Mitigation:** Seek suitable pricing data and, where feasible, validate recommendations through a properly designed experiment before deployment.

### 13.10 Reproducibility

Passing tests and generating reports do not automatically establish that the full project can be reproduced in a clean environment.

**Mitigation:** Verify the complete workflow, document dependency versions and random seeds, and ensure that documented commands regenerate the expected outputs.

## 14. Future Improvements and Development Roadmap

### Phase 1: Verify Causal Correctness

- Verify the synthetic ground-truth calculation against the data generator.
- Define the treatment, control, outcome, and target estimand explicitly.
- Ensure model estimates and reference effects represent the same causal quantity.
- Add tests for ground-truth and metric calculations.

**Goal:** A verified and reproducible DML evaluation pipeline.

### Phase 2: Improve Treatment-Effect Estimation

- Investigate multi-treatment causal estimation for the five discount levels.
- Compare suitable causal estimators using consistent data partitions.
- Measure bias, MAE, RMSE, and variability.
- Evaluate performance across repeated holdout splits.
- Report uncertainty where statistically appropriate.

**Goal:** A documented comparison of causal estimators supported by reproducible results.

### Phase 3: Develop Causal Pricing-Policy Evaluation

- Estimate the effect of each candidate discount.
- Compare fixed-discount policies with a causal-model-based policy.
- Evaluate policies on customers not used for model fitting.
- Compare estimated policy profit with the synthetic reference policy.
- Measure policy regret against the best policy under the simulation assumptions.

**Goal:** A policy-evaluation framework that connects causal estimates to pricing decisions.

### Phase 4: Conduct Sensitivity Analysis

- Vary product-cost ratios and expected units sold.
- Test alternative purchase-probability assumptions.
- Investigate different customer populations and treatment assignments.
- Identify conditions under which the preferred discount changes.
- Document uncertainty and failure cases.

**Goal:** A robustness report showing when the policy performs well and when it does not.

### Phase 5: Improve Software Quality

- Expand unit and integration tests.
- Validate generated reports and output columns.
- Fix random seeds where reproducibility is intended.
- Document dependency versions and execution commands.
- Run the full workflow from a clean environment.

**Goal:** A maintainable and reproducible project.

### Phase 6: Improve Reporting

- Plot estimated versus true treatment effects.
- Visualize estimation errors.
- Compare expected profit across pricing policies.
- Report policy regret and uncertainty where appropriate.
- Clearly label observational and synthetic results.

**Goal:** A professional report supported by reproducible charts and tables.

### Phase 7: Investigate Real-World Validation

- Identify suitable transaction, pricing, product-cost, and customer-response data.
- Check data quality, privacy, and access requirements.
- Define an appropriate validation design.
- Investigate controlled experimentation where feasible.
- Compare model recommendations with observed business outcomes before deployment.

**Goal:** A documented real-world validation plan.

## 15. Project Success Criteria

| Area | Success criterion |
|---|---|
| Causal correctness | Model and reference effects represent the same defined estimand. |
| Estimation accuracy | Bias, MAE, and RMSE are measured and compared across suitable models. |
| Robustness | Performance variability is reported across repeated evaluations. |
| Pricing decisions | Candidate policies are compared against baselines and synthetic reference policies. |
| Product-demand analysis | Observational findings and their limitations are clearly documented. |
| Profitability | Cost assumptions and excluded expenses are documented. |
| Reproducibility | Tests pass and documented commands regenerate expected outputs. |
| Reporting | Results, uncertainty, assumptions, and limitations are presented transparently. |
| Real-world readiness | Practical recommendations are withheld until appropriate validation is available. |

## 16. Team Note

EconoCausal is an exploratory data science project combining randomized marketing analysis, observational retail analytics, synthetic pricing simulation, causal inference, machine learning, and software testing.

The project investigates customer treatment effects, product-level demand patterns, and pricing-policy performance using different datasets and analytical approaches.

Its main objective is to build a reproducible analytical framework while understanding the limitations of observational and synthetic evidence.

The project is intended for research and educational purposes. Its current synthetic pricing results should not be treated as real-world business recommendations.

---

**Project:** EconoCausal — Dynamic Pricing  
**Primary tools:** Python, pandas, scikit-learn, EconML, statsmodels  
**Version control:** Git and GitHub  
**Repository:** [EconoCausal-Dynamic-Pricing](https://github.com/fahmaparveen3-arch/EconoCausal-Dynamic-Pricing)