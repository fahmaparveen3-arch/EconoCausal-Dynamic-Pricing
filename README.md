# EconoCausal — Dynamic Pricing

## Project Overview

EconoCausal is a data science project exploring causal inference, uplift modelling, and data-driven pricing decisions. It combines randomized marketing analysis with a separate synthetic discount-pricing environment to investigate customer treatment effects and pricing-policy performance.

The project uses Python, machine learning, and Double Machine Learning (DML) to estimate customer-level treatment effects in synthetic pricing data. It also compares candidate discount policies using model-based expected revenue and profit.

**Important:** The Hillstrom marketing experiment and the synthetic pricing experiment address different questions. Results from the marketing analysis do not independently validate the pricing model.

## Project Objectives

- Analyze treatment effects in a randomized marketing experiment.
- Explore customer-level treatment-effect estimation using machine learning.
- Generate and validate synthetic customer-pricing data.
- Evaluate DML estimates against known synthetic reference effects.
- Compare pricing policies using expected purchase rates, revenue, and profit.
- Build reproducible Python modules, automated tests, and evaluation reports.
- Document assumptions, estimation errors, and limitations transparently.

## Technology Stack

- **Language:** Python
- **Data analysis:** pandas, NumPy
- **Machine learning:** scikit-learn
- **Causal inference:** EconML, Double Machine Learning
- **Testing:** pytest
- **Version control:** Git and GitHub

## Project Structure

```text
EconoCausal-Dynamic-Pricing/
├── data/
│   └── prepared_pricing.csv
├── notebooks/
│   └── Exploratory analysis notebooks
├── src/
│   ├── data_processing/
│   │   ├── generate_synthetic_pricing_data.py
│   │   └── prepare_pricing_data.py
│   ├── models/
│   │   └── train_dml.py
│   ├── evaluation/
│   │   ├── compare_pricing_policies.py
│   │   ├── evaluate_pricing_profit.py
│   │   ├── validate_dml_against_truth.py
│   │   └── validate_dml_holdout.py
│   └── pricing/
│       └── dynamic_pricing.py
├── reports/
│   ├── dml_customer_effects.csv
│   ├── dml_truth_validation.csv
│   ├── dml_holdout_validation.csv
│   ├── pricing_policy_comparison.csv
│   └── pricing_profit_evaluation.csv
├── tests/
│   ├── test_dynamic_pricing.py
│   └── test_train_dml.py
├── requirements.txt
└── README.md
```

This is a simplified view of the main project files. The exact repository may contain additional files and notebooks.

## Datasets

### 1. Hillstrom randomized marketing dataset

The Hillstrom dataset contains 64,000 customer records from a randomized email-marketing experiment. It includes customer characteristics, treatment groups, visits, conversions, and spending.

The earlier analysis compared men's email and women's email campaigns with a no-email control group.

Previously recorded results:

| Analysis | Result |
|---|---:|
| Men's email vs. no email — conversion difference | +0.681 percentage points |
| Women's email vs. no email — conversion difference | +0.311 percentage points |
| Uplift model ROC-AUC | 0.5490 |
| Uplift model PR-AUC | 0.0103 |
| Previously reported mean predicted uplift | 0.632 percentage points |

These figures are from the earlier analysis and should be reproduced from the corresponding notebook or scripts before final submission.

### 2. Synthetic discount-pricing dataset

The synthetic pricing dataset contains 10,000 customer records. It represents customer characteristics, product categories, original prices, discount assignments, purchase outcomes, and generated purchase probabilities.

The dataset is used to investigate pricing strategies and evaluate treatment-effect estimates against known simulation assumptions.

Because the data are synthetic, the results demonstrate behaviour under the specified data-generating process rather than proven real-world business performance.

## Methodology

### 1. Data preparation

- Generate synthetic customer and pricing records.
- Prepare the dataset for modelling.
- Validate required columns, customer identifiers, treatment values, and outcomes.
- Use customer characteristics as model features.
- Exclude generated purchase probabilities from the DML feature set to avoid target leakage.

### 2. Double Machine Learning

The DML implementation uses EconML's `LinearDML`, random-forest nuisance models, and one-hot encoding for categorical features.

The current model represents discount assignment as a binary treatment and estimates customer-level treatment effects relative to the control condition.

**Current limitation:** The treatment combines multiple discount levels. Therefore, the model does not independently identify the causal effect of each specific discount percentage.

### 3. Ground-truth validation

Because the pricing data are synthetic, a reference treatment effect can be calculated from the known purchase-probability formula.

The validation workflow compares estimated effects with synthetic reference effects using:

- Average treatment effect (ATE).
- ATE estimation bias.
- Individual-effect mean absolute error (MAE).
- Individual-effect root mean squared error (RMSE).

### 4. Holdout evaluation

The holdout evaluation splits customers into training and test partitions. The DML model is fitted on training customers, and treatment effects are estimated for unseen test customers.

The holdout validation script compares these estimates with synthetic reference effects for the corresponding customers.

This provides an out-of-sample diagnostic. A single split, however, cannot establish that model performance is stable across all possible datasets.

### 5. Pricing-policy comparison

The policy-comparison script evaluates five candidate discount policies:

- 0%
- 5%
- 10%
- 15%
- 20%

Each policy is evaluated using the same 10,000 synthetic customers and the purchase-probability formula defined by the simulation.

The comparison includes expected purchase rate, expected revenue per customer, expected profit per customer, and total expected profit.

## Setup and Installation

Run the following commands from the project root.

### 1. Create a virtual environment

For Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If you already use a virtual environment such as `.venv313`, you can continue using it instead.

### 2. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

## Running the Project

### 1. Generate synthetic pricing data

```powershell
python src/data_processing/generate_synthetic_pricing_data.py
```

### 2. Prepare the dataset

```powershell
python src/data_processing/prepare_pricing_data.py
```

### 3. Train the DML model

```powershell
python src/models/train_dml.py
```

The model saves customer-level estimated treatment effects to:

`reports/dml_customer_effects.csv`

### 4. Evaluate pricing profit

```powershell
python src/evaluation/evaluate_pricing_profit.py
```

The results are saved to:

`reports/pricing_profit_evaluation.csv`

The report includes purchase rates, revenue, estimated product costs, and simulated profit.

### 5. Compare pricing policies

```powershell
python src/evaluation/compare_pricing_policies.py
```

The results are saved to:

`reports/pricing_policy_comparison.csv`

### 6. Validate against synthetic ground truth

```powershell
python -m src.evaluation.validate_dml_against_truth
```

The results are saved to:

`reports/dml_truth_validation.csv`

### 7. Evaluate DML on holdout customers

```powershell
python -m src.evaluation.validate_dml_holdout
```

The results are saved to:

`reports/dml_holdout_validation.csv`

### 8. Run automated tests

```powershell
python -m pytest -v
```

**Latest recorded test result: 17 passed.** Re-run the tests after code changes to verify the current state.

## Pricing-Policy Results

The following results were recorded from the synthetic policy-comparison report.

| Discount | Expected purchase rate | Expected profit per customer | Total expected profit |
|---:|---:|---:|---:|
| 0% | 20.78% | 33.24 | 332,435.25 |
| 5% | 23.54% | 33.42 | 334,186.01 |
| 10% | 26.53% | 32.85 | 328,546.76 |
| 15% | 29.72% | 31.41 | 314,052.64 |
| 20% | 33.11% | 28.93 | 289,266.88 |

Under the current simulation assumptions, the **5% discount policy** produces the highest expected profit among the five tested policies.

Its total expected profit is 334,186.01, compared with 332,435.25 for the 0% policy. This is an estimated improvement of approximately 0.53%.

The simulation illustrates that higher discounts can increase purchase rates while reducing profit per customer because the price reduction may outweigh the benefit of additional purchases.

### Assumptions

- The same synthetic customer records are used to evaluate all candidate policies.
- Expected units per purchase are assumed to be 1.15.
- Product-cost ratios are illustrative assumptions.
- Operating expenses and other business costs are excluded.
- Expected profit depends on the synthetic purchase-probability formula and its assumptions.

These results do not establish that 5% is the optimal discount for a real business.

## DML Validation Results

### 1. Ground-truth validation

Previously recorded full-dataset validation results:

| Metric | Result |
|---|---:|
| Customers evaluated | 10,000 |
| True synthetic policy ATE | 0.074463 |
| Estimated DML ATE | 0.079521 |
| ATE estimation bias | 0.005058 |
| Individual-effect MAE | 0.016636 |
| Individual-effect RMSE | 0.020166 |

The estimated average effect exceeds the synthetic reference effect. The bias and individual-effect errors quantify the discrepancy between the model estimates and the reference values.

### 2. Holdout validation

Previously recorded holdout results:

| Metric | Result |
|---|---:|
| Holdout customers evaluated | 2,500 |
| True synthetic policy ATE | 0.074861 |
| Estimated DML ATE | 0.092794 |
| ATE estimation bias | 0.017932 |
| Individual-effect MAE | 0.020994 |
| Individual-effect RMSE | 0.024203 |

The estimated holdout ATE is approximately 1.79 percentage points higher than the synthetic reference effect.

The MAE and RMSE also show that individual customer-level treatment effects are not estimated perfectly.

These are diagnostic results from a synthetic experiment. They should not be interpreted as evidence of real-world pricing performance.

## Automated Tests

The automated test suite covers:

- Discounted-price calculations.
- Zero and full discounts.
- Invalid prices and discount values.
- Purchase-probability estimation.
- Expected-profit calculations.
- Candidate-discount comparisons.
- DML input validation.
- Missing columns, duplicate customer IDs, and invalid treatment values.
- DML model fitting and finite customer-level estimates.
- Holdout evaluation and unique test-customer results.

**Latest recorded verification: 17 tests passed.**

Run the tests using:

```powershell
python -m pytest -v
```

## Limitations and Critical Analysis

### 1. Synthetic data

The pricing dataset is simulated and relies on predefined assumptions. Its results may not generalize to real customers or markets.

**Mitigation:** Evaluate the model under multiple data-generating scenarios and document the assumptions behind each experiment.

### 2. Binary treatment representation

The current DML model estimates a binary discount-versus-control effect even though the pricing comparison contains five discount levels.

**Mitigation:** Investigate multi-treatment causal estimation or separate discount-versus-control comparisons.

### 3. Treatment-effect estimation error

The holdout estimate overstates the synthetic reference ATE by approximately 1.79 percentage points.

**Mitigation:** Verify the target estimand, compare appropriate estimators, and evaluate stability across repeated holdout splits.

### 4. Limited robustness evaluation

Current validation uses a single holdout split, so the reported results may depend on the selected customers and random seed.

**Mitigation:** Repeat evaluation across suitable splits and report performance variability and uncertainty.

### 5. Simplified profit assumptions

Product costs are illustrative, and profit excludes shipping, marketing, taxes, returns, inventory costs, and operating expenses.

**Mitigation:** Make cost assumptions configurable and conduct sensitivity analysis. Use actual cost data if available.

### 6. Separate marketing and pricing experiments

The Hillstrom email experiment does not directly measure discount effects.

**Mitigation:** Keep the evaluation methods separate and connect the components only where the causal methodology supports it.

### 7. No real-world validation

The project does not yet demonstrate that its pricing recommendations improve actual business outcomes.

**Mitigation:** Seek appropriate real pricing data and, where feasible, validate recommendations through a properly designed experiment before deployment.

### 8. Reproducibility

Passing tests verifies selected software behaviour, but it does not by itself establish causal validity or production readiness.

**Mitigation:** Verify the full workflow, document dependencies and random seeds, and ensure that reports can be regenerated using the documented commands.

## Future Improvements and Development Roadmap

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
- Investigate the effect of different customer populations and treatment assignments.
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

## Project Success Criteria

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

## Team Note

EconoCausal is an exploratory project combining causal analysis, machine learning, synthetic pricing simulation, and software testing. The current implementation provides a foundation for evaluating treatment-effect estimates and pricing-policy assumptions.

The next development stage will focus on verifying causal correctness, improving multi-discount evaluation, assessing robustness, and strengthening the evidence behind pricing decisions.

The project is intended for research and educational purposes. Its current synthetic results should not be treated as real-world business recommendations.
