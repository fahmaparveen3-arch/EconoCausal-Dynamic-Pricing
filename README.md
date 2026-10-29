# EconoCausal — Dynamic Pricing

## 1. Project Overview

EconoCausal is a data science project exploring causal inference, uplift modelling, and data-driven pricing decisions. It combines a randomized marketing experiment with a separate synthetic discount-pricing environment to investigate customer treatment effects and pricing-policy performance.

The project uses Python, machine learning, and Double Machine Learning (DML) to estimate customer-level treatment effects in synthetic pricing data. It also compares candidate discount policies using model-based expected purchase rates, revenue, and profit.

**Important:** The Hillstrom marketing experiment and the synthetic pricing experiment address different questions. Results from the marketing analysis do not independently validate the pricing model.

## 2. Project Objectives

- Analyze treatment effects in a randomized marketing experiment.
- Explore customer-level treatment-effect estimation using machine learning.
- Generate and validate synthetic customer-pricing data.
- Evaluate DML estimates against known synthetic reference effects.
- Compare causal estimators using repeated train/test splits.
- Compare pricing policies using expected purchase rates, revenue, and profit.
- Build reusable Python modules, automated tests, and evaluation reports.
- Document assumptions, estimation errors, and limitations transparently.

## 3. Technology Stack

- **Programming language:** Python
- **Data analysis:** pandas, NumPy
- **Machine learning:** scikit-learn
- **Causal inference:** EconML, Double Machine Learning
- **Testing:** pytest
- **Visualization:** Matplotlib, Seaborn
- **Version control:** Git and GitHub

## 4. Project Structure

The following tree summarizes the main project files. Local datasets, notebooks, generated reports, and additional files may vary by branch.

```text
EconoCausal-Dynamic-Pricing/
├── data/
│   └── synthetic_pricing.csv
├── notebooks/
│   ├── 01_hillstrom_eda.ipynb
│   └── 01_hillstrom_eda_backup.ipynb
├── src/
│   ├── data_processing/
│   │   ├── clean_data.py
│   │   ├── generate_synthetic_pricing_data.py
│   │   ├── load_data.py
│   │   ├── load_pricing_data.py
│   │   └── prepare_pricing_data.py
│   ├── models/
│   │   ├── train_dml.py
│   │   └── train_uplift.py
│   ├── evaluation/
│   │   ├── compare_dml_estimators.py
│   │   ├── compare_pricing_policies.py
│   │   ├── evaluate_pricing_profit.py
│   │   ├── evaluate_uplift.py
│   │   ├── validate_dml_against_truth.py
│   │   └── validate_dml_holdout.py
│   └── pricing/
│       └── dynamic_pricing.py
├── reports/
│   ├── dml_customer_effects.csv
│   ├── dml_estimator_comparison.csv
│   ├── dml_estimator_repeated_seed_summary.csv
│   ├── dml_holdout_validation.csv
│   ├── dml_truth_validation.csv
│   ├── pricing_policy_comparison.csv
│   └── pricing_profit_evaluation.csv
├── tests/
│   ├── test_dynamic_pricing.py
│   └── test_train_dml.py
├── requirements.txt
├── .gitignore
└── README.md
```

The repository also contains a local backup of the estimator-comparison script. That backup is not a required project component.

## 5. Datasets

### 5.1 Hillstrom randomized marketing dataset

The Hillstrom dataset contains 64,000 customer records from a randomized email-marketing experiment. It includes customer characteristics, marketing treatment groups, visits, conversions, and spending.

The earlier analysis compared men's email and women's email campaigns with a no-email control group.

Previously recorded results:

| Analysis | Result |
|---|---:|
| Men's email vs. no email: conversion difference | +0.681 percentage points |
| Women's email vs. no email: conversion difference | +0.311 percentage points |
| Uplift model ROC-AUC | 0.5490 |
| Uplift model PR-AUC | 0.0103 |
| Previously reported mean predicted uplift | 0.632 percentage points |

These figures were recorded during earlier analysis and should be reproduced from the relevant notebook or scripts before final submission.

### 5.2 Synthetic discount-pricing dataset

The synthetic pricing dataset contains 10,000 customer records. It represents customer characteristics, product categories, discount assignments, purchase outcomes, and generated purchase probabilities.

The dataset supports experiments involving discount assignment, causal-effect estimation, and pricing-policy evaluation.

Because the data are synthetic, the results demonstrate behaviour under specified simulation assumptions rather than proven real-world business performance.

## 6. Methodology

### 6.1 Data preparation

The data-processing workflow supports:

- Loading and cleaning input data.
- Generating synthetic customer-pricing records.
- Preparing data for modelling.
- Validating required columns, customer identifiers, treatment values, and outcomes.
- Selecting customer characteristics as model features.
- Excluding generated purchase probabilities from DML features to avoid target leakage.

### 6.2 Double Machine Learning

The DML implementation uses EconML's `LinearDML`, random-forest nuisance models, and one-hot encoding for categorical features.

The pricing model represents discount assignment as a binary treatment and estimates customer-level treatment effects relative to a control condition.

**Limitation:** The binary treatment combines multiple discount levels. It does not independently identify the causal effect of each specific discount percentage.

### 6.3 Synthetic ground-truth validation

Because the pricing data are generated using a known simulation process, reference treatment effects can be calculated from the underlying purchase-probability formula.

The validation workflow compares estimated effects with synthetic reference effects using:

- Average treatment effect (ATE).
- ATE estimation bias.
- Individual-effect mean absolute error (MAE).
- Individual-effect root mean squared error (RMSE).

These metrics quantify estimation error under the specified simulation. They do not establish real-world causal validity.

### 6.4 Holdout evaluation

The holdout evaluation divides customers into training and test partitions. The model is fitted using training data, and estimates are evaluated on unseen test customers.

Comparing estimated effects with synthetic reference effects provides an out-of-sample diagnostic. Results from a single split may depend on the chosen random seed and customer partition.

### 6.5 Repeated-seed estimator comparison

The estimator-comparison workflow evaluates LinearDML and NonParamDML using five random seeds: 42, 7, 21, 35, and 99.

For each seed, the workflow uses a stratified train/test split, fits the estimators, and compares their estimates against synthetic reference effects. Both estimators use the same split for each seed.

The reported metrics include:

- True and estimated ATE.
- ATE bias.
- Individual-effect MAE and RMSE.
- Correlation between estimated and reference individual effects.
- Mean and standard deviation of metrics across the repeated runs.

The repeated-seed evaluation helps assess sensitivity to data partitioning. It is not equivalent to evaluation on five independent real-world datasets.

### 6.6 Pricing-policy comparison

The pricing-policy comparison evaluates five candidate discount levels:

- 0%
- 5%
- 10%
- 15%
- 20%

The comparison uses the same synthetic customer population for all candidate policies and the purchase-probability formula defined by the simulation.

The report includes expected purchase rate, expected revenue per customer, expected profit per customer, and total expected profit.

## 7. Setup and Installation

Run the commands from the project root in Windows PowerShell.

### 7.1 Create a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If you already use the project's `.venv313` environment, you can continue using it instead.

### 7.2 Install dependencies

```powershell
python -m pip install -r requirements.txt
```

The project currently lists its principal dependencies in `requirements.txt`. Reproducibility can be improved by documenting and pinning the versions verified in the working environment.

## 8. Running the Project

Use the commands below from the project root. Confirm that the required input data are available before running each script.

### 8.1 Generate synthetic pricing data

```powershell
python src/data_processing/generate_synthetic_pricing_data.py
```

### 8.2 Prepare the pricing dataset

```powershell
python src/data_processing/prepare_pricing_data.py
```

### 8.3 Train the DML model

```powershell
python src/models/train_dml.py
```

The model writes customer-level estimated treatment effects to:

`reports/dml_customer_effects.csv`

### 8.4 Evaluate pricing profit

```powershell
python src/evaluation/evaluate_pricing_profit.py
```

The report is saved to:

`reports/pricing_profit_evaluation.csv`

### 8.5 Compare pricing policies

```powershell
python src/evaluation/compare_pricing_policies.py
```

The report is saved to:

`reports/pricing_policy_comparison.csv`

### 8.6 Validate against synthetic ground truth

```powershell
python -m src.evaluation.validate_dml_against_truth
```

The report is saved to:

`reports/dml_truth_validation.csv`

### 8.7 Evaluate DML on holdout customers

```powershell
python -m src.evaluation.validate_dml_holdout
```

The report is saved to:

`reports/dml_holdout_validation.csv`

### 8.8 Compare DML estimators across repeated seeds

```powershell
python src/evaluation/compare_dml_estimators.py
```

The current comparison script generates the repeated-seed summary at:

`reports/dml_estimator_repeated_seed_summary.csv`

The single-split estimator comparison report at `reports/dml_estimator_comparison.csv` contains previously generated results. The current comparison script does not regenerate that single-split report.

### 8.9 Run automated tests

```powershell
python -m pytest -v
```

**Last verified test result:** 26 tests passed across `tests/test_dynamic_pricing.py` and `tests/test_train_dml.py`. This is the last recorded result for those two files, not a claim that the entire project test suite has been rerun. Run the full test suite before final submission.

## 9. Pricing-Policy Results

The following results were previously recorded from the synthetic policy-comparison report.

| Discount | Expected purchase rate | Expected profit per customer | Total expected profit |
|---:|---:|---:|---:|
| 0% | 20.78% | 33.24 | 332,435.25 |
| 5% | 23.54% | 33.42 | 334,186.01 |
| 10% | 26.53% | 32.85 | 328,546.76 |
| 15% | 29.72% | 31.41 | 314,052.64 |
| 20% | 33.11% | 28.93 | 289,266.88 |

Under the current simulation assumptions, the **5% discount policy** produces the highest expected profit among the five tested policies.

Its total expected profit is 334,186.01, compared with 332,435.25 for the no-discount policy. This represents an estimated improvement of approximately 0.53%.

The simulation illustrates a trade-off: larger discounts increase estimated purchase rates, but the resulting reduction in selling price can outweigh the benefit of additional purchases.

### Assumptions

- The same synthetic customer records are used to evaluate all candidate policies.
- Expected units per purchase are assumed to be 1.15.
- Product-cost ratios are illustrative assumptions.
- Operating expenses and other business costs are excluded.
- Expected profit depends on the synthetic purchase-probability formula and its assumptions.

These results do not establish that 5% is the optimal discount for a real business.

## 10. DML Validation Results

The following are previously recorded results. They should be regenerated and verified before final submission.

### 10.1 Full-dataset synthetic ground-truth validation

| Metric | Result |
|---|---:|
| Customers evaluated | 10,000 |
| True synthetic policy ATE | 0.074463 |
| Estimated DML ATE | 0.079521 |
| ATE estimation bias | 0.005058 |
| Individual-effect MAE | 0.016636 |
| Individual-effect RMSE | 0.020166 |

The estimated average effect exceeds the synthetic reference effect. The bias and individual-effect errors quantify the discrepancy between model estimates and the reference values.

### 10.2 Holdout validation

| Metric | Result |
|---|---:|
| Holdout customers evaluated | 2,500 |
| True synthetic policy ATE | 0.074861 |
| Estimated DML ATE | 0.092794 |
| ATE estimation bias | 0.017932 |
| Individual-effect MAE | 0.020994 |
| Individual-effect RMSE | 0.024203 |

The estimated holdout ATE is approximately 1.79 percentage points higher than the synthetic reference effect.

The MAE and RMSE also show that individual customer-level treatment effects are not estimated perfectly. These results are diagnostics for a synthetic experiment, not evidence of real-world pricing performance.

### 10.3 Repeated-seed estimator comparison

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

In this experiment, LinearDML has lower mean MAE and RMSE and higher mean correlation with the synthetic reference effects than NonParamDML. Both estimators have a positive mean ATE bias in the recorded runs.

The findings support choosing LinearDML as the stronger candidate for further investigation under this particular simulation. They do not prove that it is universally superior or that either model will perform similarly on real customer data.

## 11. Automated Tests

The current test files cover areas including:

- Discounted-price calculations.
- Zero and full discounts.
- Invalid prices and discount values.
- Purchase-probability estimation.
- Expected-profit calculations.
- Candidate-discount comparisons.
- DML input validation.
- Missing columns, duplicate customer IDs, and invalid treatment values.
- Handling of invalid numeric values.
- DML model fitting and finite customer-level estimates.
- Holdout evaluation and unique test-customer results.

The last recorded test run reported **26 passed** for the two existing test files. The full suite should be rerun before final submission to verify the current repository state.

Passing tests confirms selected software behaviours; it does not by itself establish causal correctness or production readiness.

## 12. Limitations and Critical Analysis

### 12.1 Synthetic data

The pricing dataset is simulated using predefined assumptions. Its results may not generalize to real customers or markets.

**Mitigation:** Evaluate alternative data-generating scenarios and document the assumptions behind each experiment.

### 12.2 Binary treatment representation

The current DML model estimates a binary discount-versus-control effect even though the policy comparison contains five discount levels.

**Mitigation:** Investigate multi-treatment causal estimation or appropriately defined discount-versus-control comparisons.

### 12.3 Treatment-effect estimation error

The recorded holdout estimate overstates the synthetic reference ATE by approximately 1.79 percentage points.

**Mitigation:** Verify the target estimand, compare suitable estimators, and evaluate stability across repeated holdout splits.

### 12.4 Limited robustness evaluation

Repeated-seed evaluation provides more evidence than a single split, but five runs on the same synthetic dataset do not establish generalization across different populations or data-generating processes.

**Mitigation:** Conduct additional robustness checks and report variability and uncertainty where appropriate.

### 12.5 Simplified profit assumptions

Product costs are illustrative, and the simulation excludes shipping, marketing, taxes, returns, inventory costs, and operating expenses.

**Mitigation:** Make cost assumptions configurable and conduct sensitivity analysis. Use actual cost data if available.

### 12.6 Separate marketing and pricing experiments

The Hillstrom email experiment does not directly measure discount effects.

**Mitigation:** Keep the evaluation methods separate and connect the components only where the causal methodology supports it.

### 12.7 No real-world validation

The project does not yet demonstrate that its pricing recommendations improve actual business outcomes.

**Mitigation:** Seek suitable pricing data and, where feasible, validate recommendations through a properly designed experiment before deployment.

### 12.8 Reproducibility

Passing tests and generating reports do not automatically establish that the full project can be reproduced in a clean environment.

**Mitigation:** Verify the full workflow, document dependency versions and random seeds, and ensure that the documented commands regenerate the expected outputs.

## 13. Future Improvements and Development Roadmap

### Phase 1: Verify causal correctness

- Verify the synthetic ground-truth calculation against the data generator.
- Define the treatment, control, outcome, and target estimand explicitly.
- Ensure model estimates and reference effects represent the same causal quantity.
- Add tests for ground-truth and metric calculations.

**Goal:** A verified and reproducible DML evaluation pipeline.

### Phase 2: Improve treatment-effect estimation

- Investigate multi-treatment causal estimation for the five discount levels.
- Compare suitable causal estimators using consistent data partitions.
- Measure bias, MAE, RMSE, and variability.
- Evaluate performance across repeated holdout splits.
- Report uncertainty where statistically appropriate.

**Goal:** A documented comparison of causal estimators supported by reproducible results.

### Phase 3: Develop causal pricing-policy evaluation

- Estimate the effect of each candidate discount.
- Compare fixed-discount policies with a causal-model-based policy.
- Evaluate policies on customers not used for model fitting.
- Compare estimated policy profit with the synthetic reference policy.
- Measure policy regret against the best policy under the simulation assumptions.

**Goal:** A policy-evaluation framework that connects causal estimates to pricing decisions.

### Phase 4: Conduct sensitivity analysis

- Vary product-cost ratios and expected units sold.
- Test alternative purchase-probability assumptions.
- Investigate different customer populations and treatment assignments.
- Identify conditions under which the preferred discount changes.
- Document uncertainty and failure cases.

**Goal:** A robustness report showing when the policy performs well and when it does not.

### Phase 5: Improve software quality

- Expand unit and integration tests.
- Validate generated reports and output columns.
- Fix random seeds where reproducibility is intended.
- Document dependency versions and execution commands.
- Run the full workflow from a clean environment.

**Goal:** A maintainable and reproducible project.

### Phase 6: Improve reporting

- Plot estimated versus true treatment effects.
- Visualize estimation errors.
- Compare expected profit across pricing policies.
- Report policy regret and uncertainty where appropriate.
- Clearly label synthetic results and assumptions.

**Goal:** A professional report supported by reproducible charts and tables.

### Phase 7: Investigate real-world validation

- Identify suitable transaction, pricing, product-cost, and customer-response data.
- Check data quality, privacy, and access requirements.
- Define an appropriate validation design.
- Investigate controlled experimentation where feasible.
- Compare model recommendations with observed business outcomes before deployment.

**Goal:** A documented real-world validation plan. Deployment should remain out of scope until suitable evidence and safeguards are available.

## 14. Project Success Criteria

| Area | Success criterion |
|---|---|
| Causal correctness | Model and reference effects represent the same defined estimand. |
| Estimation accuracy | Bias, MAE, and RMSE are measured and compared across suitable models. |
| Robustness | Performance variability is reported across repeated evaluations. |
| Pricing decisions | Candidate policies are compared against baselines and the synthetic reference policy. |
| Profitability | Cost assumptions and excluded expenses are documented. |
| Reproducibility | Tests pass and documented commands regenerate the expected outputs. |
| Reporting | Results, uncertainty, assumptions, and limitations are presented transparently. |
| Real-world readiness | Practical recommendations are withheld until appropriate validation is available. |

## 15. Team Note

EconoCausal is an exploratory project combining causal analysis, machine learning, synthetic pricing simulation, and software testing. The current implementation provides a foundation for evaluating treatment-effect estimates and pricing-policy assumptions.

The next development stage will focus on verifying causal correctness, improving multi-discount evaluation, assessing robustness, and strengthening the evidence behind pricing decisions.

The project is intended for research and educational purposes. Its current synthetic results should not be treated as real-world business recommendations.