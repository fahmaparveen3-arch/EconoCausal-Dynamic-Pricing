# EconoCausal — Causal Inference and Dynamic Pricing

An applied data science project combining causal inference, machine learning, customer analytics, and pricing-policy evaluation.

## 1. Project Overview

EconoCausal explores how data science and causal inference can support business decisions involving customer behaviour, marketing interventions, and pricing strategies.

The project brings together three complementary analytical components:

1. **Randomized marketing analysis:** Uses the Hillstrom Email Marketing dataset to investigate the effects of email campaigns on customer visits and conversions.
2. **Observational retail analysis:** Uses the UCI Online Retail dataset to explore product sales, prices, quantities, and demand patterns.
3. **Synthetic dynamic-pricing experiment:** Uses generated customer data with known simulation assumptions to evaluate treatment-effect estimators and compare discount policies.

These components address different analytical questions. The randomized marketing experiment, observational retail analysis, and synthetic pricing experiment are evaluated separately rather than being treated as one common causal experiment.

## 2. Project Objectives

The main objectives are to:

- Analyse the effects of marketing interventions on customer behaviour.
- Explore historical retail sales, product prices, and quantities.
- Apply machine learning and causal inference techniques to estimate treatment effects.
- Compare causal estimators against a Difference-in-Means baseline.
- Evaluate estimator performance using known synthetic reference effects.
- Investigate the stability of estimates across different train/test partitions.
- Compare discount policies using expected purchase probability and expected profit.
- Build a reproducible and documented Python project with reusable modules and automated tests.

## 3. Technology Stack

| Area | Tools and Libraries |
|---|---|
| Programming language | Python |
| Data manipulation | Pandas, NumPy |
| Data visualisation | Matplotlib, Seaborn |
| Machine learning | Scikit-learn |
| Causal inference | EconML |
| Statistical analysis | SciPy, Statsmodels |
| Development environment | VS Code, Jupyter Notebook |
| Version control | Git and GitHub |
| Testing | Pytest |
| Data storage | CSV |

## 4. Project Structure

The repository is organised into data-processing, pricing, modelling, evaluation, testing, notebook, and reporting components.

The following tree shows the principal source files and directories inspected in the repository. It is a simplified view and does not list every dataset, notebook, backup, cache, or generated file.

```text
EconoCausal-Dynamic-Pricing/
│
├── data/
│   ├── hillstrom.csv
│   ├── prepared_pricing.csv
│   ├── synthetic_pricing.csv
│   ├── online+retail/
│   └── processed/
│       ├── online_retail_cleaned.csv
│       ├── online_retail_product_sales.csv
│       ├── online_retail_excluded.csv
│       ├── online_retail_fully_reversed_audit.csv
│       ├── online_retail_non_product_audit.csv
│       └── online_retail_returns_cancellations.csv
│
├── notebooks/
│   ├── 01_hillstrom_eda.ipynb
│   └── 02_online_retail_eda.ipynb
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
│   ├── pricing/
│   │   └── dynamic_pricing.py
│   │
│   └── evaluation/
│       ├── compare_discount_causal_effects.py
│       ├── compare_dml_estimators.py
│       ├── compare_pricing_policies.py
│       ├── evaluate_pricing_profit.py
│       ├── evaluate_uplift.py
│       ├── validate_dml_against_truth.py
│       └── validate_dml_holdout.py
│
├── reports/
│
├── tests/
│   ├── test_dynamic_pricing.py
│   └── test_compare_dml_estimators.py
│
├── README.md
├── README_backup.md
├── requirements.txt
└── update_online_retail_notebook.py
```

The `reports/` directory contains generated evaluation results and pricing-policy reports. The `notebooks/` directory contains the project's exploratory analysis notebooks.

## 5. Datasets

### 5.1 Hillstrom Email Marketing Dataset

The Hillstrom dataset contains 64,000 customers from a randomized email marketing experiment.

It includes customer characteristics, marketing treatment groups, website visits, conversions, and spending information.

Important columns include:

- `recency`
- `history_segment`
- `history`
- `mens`
- `womens`
- `zip_code`
- `newbie`
- `channel`
- `segment`
- `visit`
- `conversion`
- `spend`

The dataset contains three experimental groups:

- Men's E-Mail
- Women's E-Mail
- No E-Mail

The randomized treatment assignment makes this dataset useful for investigating the effects of marketing emails on customer outcomes.

The verified analysis recorded the following results:

| Comparison or Metric | Result |
|---|---:|
| Men's email vs. no email — conversion effect | +0.681 percentage points |
| Women's email vs. no email — conversion effect | +0.311 percentage points |
| Baseline conversion model ROC-AUC | 0.5490 |
| Baseline conversion model PR-AUC | 0.0103 |
| Mean predicted uplift from the T-learner | 0.632 percentage points |
| T-learner Qini coefficient | 0.8665 |
| Estimated incremental conversions | 35.707 |

The conversion effects are estimated from the randomized experiment. The predicted uplift and Qini results are model-based evaluation measures and should be interpreted separately from the observed group-level treatment effects.

These results describe the analysed dataset and modelling setup; they do not establish that individual customer treatment effects can be predicted with certainty.

The expected dataset location is:

```text
data/hillstrom.csv
```

Place the Hillstrom CSV file at this location before running the Hillstrom notebook.

### 5.2 UCI Online Retail Dataset

The Online Retail dataset contains transactional records from a UK-based online retailer.

It is used for exploratory analysis of:

- Product sales.
- Unit prices.
- Quantities purchased.
- Revenue patterns.
- Product-level demand behaviour.
- Relationships between price and quantity.

**Dataset source:** [UCI Machine Learning Repository — Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail)

The original Excel dataset is expected at:

```text
data/online+retail/Online Retail.xlsx
```

This dataset is observational. Relationships found between prices and quantities should not automatically be interpreted as causal price effects.

### 5.3 Synthetic Dynamic-Pricing Dataset

A separate synthetic dataset was generated for the dynamic-pricing experiment.

It contains 10,000 synthetic customers and is used to evaluate discount-treatment effects under known data-generating assumptions.

The synthetic dataset includes customer characteristics such as:

- Age.
- Income.
- Previous purchases.
- Product category.
- Treatment assignment.
- Discount rate.
- Purchase outcome.

The synthetic experiment makes it possible to compare estimated treatment effects against reference effects calculated from the simulation's purchase-probability model.

**Important:** Synthetic results are useful for controlled testing. They do not establish real-world pricing effectiveness.

## 6. Data Preprocessing

### 6.1 Hillstrom Data

The Hillstrom dataset was loaded and inspected before analysis.

The earlier data inspection recorded:

- 64,000 rows.
- 12 columns.
- No missing values in the inspected dataset.
- Three marketing treatment groups.

The marketing analysis used the Men's E-Mail and No E-Mail groups for the principal comparison.

### 6.2 Online Retail Data

The Online Retail data required cleaning before product-level analysis.

The verified row counts for the original and currently available processed files are:

| Dataset Stage | Verified Rows |
|---|---:|
| Original dataset | 541,909 |
| Cleaned dataset | 524,110 |
| Product-sales dataset | 521,755 |
| Excluded dataset | 1,176 |

The cleaned product-sales dataset was checked for duplicate records, missing product descriptions, invalid quantities, invalid prices, and revenue inconsistencies.

Previously recorded validation results included:

- No duplicate rows in the product-sales dataset.
- No missing product descriptions.
- No invalid quantity or price records.
- No revenue discrepancies.
- CustomerID missingness of approximately 25.2%.

The current verified product-sales count is **521,755 records**. Earlier documentation contained a different count; the verified processed CSV row count is used in this README.

### 6.3 Synthetic Pricing Data

The synthetic pricing data was generated using a controlled probability model.

The generator uses customer characteristics and discount rates to calculate purchase probabilities. A binary purchase outcome is then generated from those probabilities.

Treatment assignment is randomized, and treated customers receive one of the tested positive discount levels.

This controlled design allows the project to compare estimated effects with reference effects calculated from the simulation.

## 7. Methodology

### 7.1 Hillstrom Marketing Causal Analysis

The Hillstrom analysis investigates whether email marketing interventions affect customer visits and conversions using a randomized marketing experiment.

The principal comparison uses:

- **Treatment group:** Men's E-Mail.
- **Control group:** No E-Mail.
- **Outcome:** Customer conversion.

The Women's E-Mail group is also examined separately.

The observed conversion-rate differences were:

- Men's E-Mail compared with No E-Mail: +0.681 percentage points.
- Women's E-Mail compared with No E-Mail: +0.311 percentage points.

A T-learner approach was used to estimate customer-level treatment-effect predictions. The mean predicted uplift was 0.632 percentage points, with a Qini coefficient of 0.8665 and an estimated 35.707 incremental conversions.

These individual uplift values are model predictions, not directly observed individual causal effects. The uplift ranking results are exploratory, and the ranking performance was not consistently monotonic across customer groups.

A paired bootstrap comparison of Random Forest and HistGradientBoosting Qini performance produced an estimated difference of 1.4925, with a 95% confidence interval of [-3.2586, 6.4940]. Since this interval includes zero, the analysis does not provide statistically supported evidence that HistGradientBoosting outperforms Random Forest.

The results are specific to the Hillstrom dataset, selected treatment comparison, and fitted models. They should not be interpreted as proof of reliable individual-level uplift prediction in other populations.

### 7.2 Causal Machine Learning

The project uses Double Machine Learning (DML) to estimate treatment effects in the synthetic pricing experiment.

The two DML estimators evaluated are:

- LinearDML.
- NonParamDML with Gradient Boosting.

The modelling workflow uses machine-learning nuisance models to estimate the relevant outcome and treatment relationships before estimating treatment effects.

The project also compares the DML estimates against a Difference-in-Means baseline.

### 7.3 Synthetic Ground-Truth Validation

Because the synthetic purchase-probability model is known, reference treatment effects can be calculated from the simulation assumptions.

The estimated treatment effects are compared with these reference effects using:

- ATE bias.
- Mean Absolute Error (MAE).
- Root Mean Squared Error (RMSE).
- Effect correlation.

This helps distinguish average treatment-effect accuracy from individual treatment-effect prediction performance.

### 7.4 Dynamic Pricing and Expected Profit

The pricing component estimates purchase probability under different discount levels.

It evaluates candidate discounts of:

- 0%
- 5%
- 10%
- 15%
- 20%

Expected profit is calculated using the model-based purchase probability and the illustrative product-cost assumptions.

The comparison uses the same 10,000 synthetic customers for all five candidate policies.

### 7.5 Repeated-Seed DML Evaluation

To investigate sensitivity to train/test partitions, the Difference-in-Means baseline and both DML estimators were evaluated across five random seeds:

`42, 7, 21, 35, 99`

The dataset was divided using a 75% training and 25% holdout split, stratified by treatment assignment.

Each run used:

- 7,500 training customers.
- 2,500 holdout customers.

The same evaluation seeds and corresponding training and holdout splits were used for all three estimators.

### 7.6 Online Retail Price and Demand Analysis

The Online Retail analysis explores product-level relationships between unit price and quantity sold.

It includes product-level correlation analysis and a pooled regression.

The analysis is exploratory because the dataset is observational and product prices may be influenced by factors other than demand.

### 7.7 Online Retail Exploratory Results

The recorded product-level correlation results were:

| Product | Price-Quantity Correlation | p-value |
|---|---:|---:|
| Lunch Bag Red Retrospot | -0.3388 | 0.2575 |
| Regency Cake Stand | +0.1956 | 0.5219 |
| Party Bunting | -0.0916 | 0.7660 |
| Jumbo Bag | +0.1329 | 0.6652 |
| White Hanging Heart | +0.0809 | 0.7928 |

The recorded pooled regression results were:

| Metric | Result |
|---|---:|
| Price coefficient | +0.3691 |
| Standard error | 1.2321 |
| t-statistic | 0.2995 |
| p-value | 0.7658 |
| Observations | 65 |
| Residual degrees of freedom | 47 |

The analysis did not identify a statistically significant price-quantity relationship for any of the five selected products or in the pooled regression. All product-level correlation p-values and the pooled regression p-value were above the 0.05 significance level.

These results indicate that the analysis did not find statistically significant evidence of a linear price-quantity association in the selected observations. The findings should be treated as exploratory and observational, not as causal estimates of price elasticity.
## 8. Setup and Installation

### 8.1 Clone the Repository

```bash
git clone https://github.com/fahmaparveen3-arch/EconoCausal-Dynamic-Pricing.git
```

### 8.2 Move into the Project Directory

```bash
cd EconoCausal-Dynamic-Pricing
```

### 8.3 Python Version

The project was developed and tested in a Python 3.13.16 environment.

Python 3.13 is used for the current project environment.

### 8.4 Create a Virtual Environment

On Windows PowerShell:

```powershell
python -m venv .venv
```

### 8.5 Activate the Virtual Environment

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell prevents activation, use the following command in the current terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again.

### 8.6 Install Dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The project was also developed and tested in an environment named `.venv313`.

To activate that existing environment on the development machine, use:

```powershell
.\.venv313\Scripts\Activate.ps1
```

Alternatively, commands can be run directly using:

```powershell
.\.venv313\Scripts\python.exe
```

## 9. Running the Project

Run project commands from the repository root.

### 9.1 Generate Synthetic Pricing Data

```powershell
python -m src.data_processing.generate_synthetic_pricing_data
```

### 9.2 Compare Pricing Policies

```powershell
python -m src.evaluation.compare_pricing_policies
```

### 9.3 Run Automated Tests

```powershell
python -m pytest -q
```

### 9.4 Compare DML Estimators Across Repeated Seeds

Run from the project root:

```powershell
python -m src.evaluation.compare_dml_estimators
```

Outputs:

- `reports/dml_estimator_repeated_seed_results.csv` — detailed results for each estimator and random seed.
- `reports/dml_estimator_repeated_seed_summary.csv` — aggregated performance metrics across the five seeds.

The single-split estimator comparison report contains previously generated results and is not regenerated by the current repeated-seed script.

### 9.5 Online Retail Data Preprocessing

The Online Retail preprocessing workflow is part of the project's data-preparation stage.

The preprocessing source file is:

```text
src/data_processing/preprocess_online_retail.py
```

Before running the script, ensure the original Excel dataset is located at:

```text
data/online+retail/Online Retail.xlsx
```

Run the preprocessing command from the repository root:

```powershell
python -m src.data_processing.preprocess_online_retail
```

The verified preprocessing run produced the following files in `data/processed/`:

- `online_retail_cleaned.csv`
- `online_retail_product_sales.csv`
- `online_retail_non_product_audit.csv`
- `online_retail_returns_cancellations.csv`
- `online_retail_excluded.csv`
- `online_retail_fully_reversed_audit.csv`

The verified product-sales dataset contains 521,755 records.

### 9.6 Run Hillstrom Analysis

The Hillstrom exploratory analysis is available in:

```text
notebooks/01_hillstrom_eda.ipynb
```

Ensure the dataset is placed at:

```text
data/hillstrom.csv
```

Open the notebook using Jupyter Notebook or VS Code and run all cells.

The notebook uses the project's shared data-loading module.

### 9.7 Run Online Retail Analysis

The Online Retail exploratory analysis is available in:

```text
notebooks/02_online_retail_eda.ipynb
```

First, run the preprocessing command in Section 9.5.

The processed product-sales dataset should then be available at:

```text
data/processed/online_retail_product_sales.csv
```

Open the notebook using Jupyter Notebook or VS Code and run all cells.

The notebook loads the processed dataset from the project directory.

## 10. Pricing-Policy Results

The synthetic pricing experiment compared five discount policies using the same 10,000 synthetic customers.

### 10.1 Expected Profit Comparison

| Discount | Expected Purchase Rate | Expected Profit per Customer | Total Expected Profit |
|---|---:|---:|---:|
| 0% | 20.78% | 33.24 | 332,435.25 |
| 5% | 23.54% | 33.42 | 334,186.01 |
| 10% | 26.53% | 32.85 | 328,546.76 |
| 15% | 29.72% | 31.41 | 314,052.64 |
| 20% | 33.11% | 28.93 | 289,266.88 |

### 10.2 Interpretation

The 5% discount produced the highest model-based expected profit among the five tested policies.

Its expected profit was:

- 334,186.01 for the 5% discount.
- 332,435.25 for the no-discount policy.

The improvement over the no-discount policy was approximately 0.53%.

The results illustrate a trade-off between purchase probability and profit. Larger discounts increased the estimated purchase rate, but they also reduced expected profit per customer.

**Limitation:** The results use synthetic customers and illustrative product-cost assumptions. They do not establish that a 5% discount is optimal for a real business.

## 11. DML Validation Results

### 11.1 Full-Dataset Validation

The recorded full-dataset validation results were:

| Metric | Result |
|---|---:|
| True ATE | 0.074463 |
| Estimated ATE | 0.079521 |
| ATE Bias | +0.005058 |
| MAE | 0.016636 |
| RMSE | 0.020166 |

### 11.2 Holdout Validation

The recorded holdout validation results were:

| Metric | Result |
|---|---:|
| Holdout customers | 2,500 |
| True ATE | 0.074861 |
| Estimated ATE | 0.092794 |
| ATE Bias | +0.017932 |
| MAE | 0.020994 |
| RMSE | 0.024203 |

The initial holdout estimate was higher than the synthetic reference ATE. This motivated the repeated-seed evaluation.

### 11.3 Repeated-Seed Evaluation

The Difference-in-Means baseline and both DML estimators were evaluated across five random seeds: 42, 7, 21, 35, and 99. All three estimators used identical training and holdout partitions for each seed.

Each run used 7,500 training customers and 2,500 holdout customers. The reference effects were calculated from the known synthetic purchase-probability model.

The recorded DML results were:

| Metric | LinearDML | NonParamDML |
|---|---:|---:|
| Number of runs | 5 | 5 |
| Holdout customers per run | 2,500 | 2,500 |
| Mean true ATE | 0.074503 | 0.074503 |
| Mean estimated ATE | 0.078459 | 0.078441 |
| Mean signed ATE bias | +0.003956 | +0.003938 |
| Standard deviation of ATE bias | 0.008500 | 0.007810 |
| Mean MAE | 0.018963 | 0.035780 |
| Mean RMSE | 0.023124 | 0.050144 |
| Mean effect correlation | 0.617833 | 0.231091 |

**Mean Absolute ATE Bias Across Five Seeds**

| Estimator | Mean Absolute ATE Bias |
|---|---:|
| Difference-in-Means baseline | 0.006121 |
| LinearDML | 0.006120 |
| NonParamDML | 0.005975 |

The three estimators produced very similar mean absolute ATE bias. NonParamDML had the lowest value, while LinearDML was effectively tied with the Difference-in-Means baseline at the reported precision.

LinearDML performed better on individual treatment-effect prediction metrics, including MAE, RMSE, and effect correlation.

The Difference-in-Means estimator estimates an aggregate treatment effect rather than individual customer effects. Therefore, individual-effect MAE, RMSE, and correlation are not applicable to this baseline and are not reported.

These metrics measure different aspects of estimator performance. Lower average treatment-effect bias does not necessarily imply better individual treatment-effect predictions.

### 11.4 Seed 42 Investigation

Seed 42 showed greater sensitivity than the other evaluated partitions.

The raw treatment-group purchase-rate difference was approximately:

- Training set: 9.07%.
- Holdout set: 3.72%.

Both DML estimators produced estimates above the synthetic reference ATE for this partition:

- LinearDML estimated ATE: 0.092794.
- NonParamDML estimated ATE: 0.090849.
- True ATE: 0.074861.

The estimates were close to the training-set raw treatment difference, while the holdout raw treatment difference was substantially smaller.

This suggests sensitivity to the train/test partition and variation in observed treatment-group outcomes. It does not establish overfitting or identify a definitive cause.

### 11.5 Train/Test Split-Ratio Validation

To investigate the sensitivity of DML estimates to different training and holdout sample sizes, three train/test split ratios were evaluated: 70/30, 75/25, and 80/20.

The experiment used the synthetic pricing dataset, random seed 42, and stratified treatment assignment for all three configurations.

**Validation Results**

| Metric | 70/30 | 75/25 | 80/20 |
|---|---:|---:|---:|
| Training customers | 7,000 | 7,500 | 8,000 |
| Holdout customers | 3,000 | 2,500 | 2,000 |
| True ATE | 0.074993 | 0.074861 | 0.074851 |
| Estimated ATE | 0.091989 | 0.092794 | 0.084694 |
| Absolute ATE bias | 0.016996 | 0.017932 | 0.009843 |
| MAE | 0.027921 | 0.020994 | 0.016179 |
| RMSE | 0.030298 | 0.024203 | 0.019871 |

**Interpretation**

The 80/20 configuration produced the lowest absolute ATE bias, MAE, and RMSE among the three tested configurations. The 75/25 configuration performed better than 70/30 on MAE and RMSE, while the 70/30 configuration had the largest individual-effect prediction errors.

All three configurations overestimated the synthetic reference ATE.

These findings indicate that the training and holdout sample allocation can influence treatment-effect estimates and individual-effect prediction errors.

**Limitation:** This initial comparison used one random seed (42). Therefore, the results do not establish that 80/20 is universally optimal. Additional repeated-seed evaluation is required to determine whether the observed differences remain consistent across alternative partitions.

**Evaluation script:** `src/evaluation/validate_dml_split_ratios.py`

**Generated report:** `reports/dml_split_ratio_validation.csv`

### 11.6 Repeated-Seed Train/Test Split-Ratio Validation

To evaluate the stability of DML performance across different training and holdout sample allocations, three split ratios were tested: 70/30, 75/25, and 80/20.

Each split ratio was evaluated using five random seeds: 42, 7, 21, 35, and 99. LinearDML was trained using the same model configuration across all experiments, with preprocessing fitted only on training data.

A total of 15 experiments were completed.

**Repeated-Seed Validation Results**

| Metric (Mean Across 5 Seeds) | 70/30 | 75/25 | 80/20 |
|---|---:|---:|---:|
| Absolute ATE Bias | 0.008115 | 0.006120 | 0.004011 |
| MAE | 0.021871 | 0.018963 | 0.018335 |
| RMSE | 0.026420 | 0.023124 | 0.022395 |
| Effect Correlation | 0.606872 | 0.617833 | 0.587684 |

**Interpretation**

The 80/20 split achieved the lowest mean absolute ATE bias, MAE, and RMSE among the tested configurations. The 75/25 split achieved the highest mean effect correlation.

The 80/20 split also showed the lowest standard deviation in absolute ATE bias (0.003564), indicating greater consistency in ATE estimation across the five tested seeds.

All three configurations produced positive mean ATE bias, indicating slight overestimation of the synthetic reference effect.

These findings suggest that an 80/20 split provides the strongest overall performance among the configurations evaluated. However, the results do not establish that it is universally optimal.

**Limitation:** The experiment used five random seeds on one synthetic dataset. Further validation on additional datasets and alternative model configurations would strengthen the findings.

**Evaluation script:** `src/evaluation/validate_dml_repeated_split_ratios.py`

**Individual results:** `reports/dml_repeated_split_ratios_results.csv`

**Summary report:** `reports/dml_repeated_split_ratios_summary.csv`


### 11.7 Repeated-Seed Holdout Validation Against Synthetic Ground Truth

To address the limitation of in-sample validation, an independent holdout validation was performed using `evaluate_dml_holdout()`.

LinearDML was evaluated using five random seeds: 42, 7, 21, 35, and 99. Each experiment used a 75/25 train-test split, resulting in 2,500 holdout customers per run.

The synthetic ground-truth treatment effects were calculated using the known purchase-probability formula. The benchmark incorporated the actual discount distribution among treated customers:

| Discount Level | Actual Proportion |
|---|---:|
| 5% | 25.14% |
| 10% | 24.69% |
| 15% | 25.86% |
| 20% | 24.31% |

The project uses two discount-weighting approaches for different evaluation purposes:

- **Actual-distribution weighting:** The average treatment effect uses the observed proportions of the four discount levels among treated customers. This represents the actual discount distribution in the generated dataset.
- **Equal weighting:** Each discount level (5%, 10%, 15%, and 20%) receives a 25% weight, regardless of its observed frequency. This gives all four discount levels equal importance.

These approaches estimate different average treatment effects and should be interpreted separately. Their results are not directly interchangeable.

**Repeated-Seed Holdout Results**

| Metric | Mean | Standard Deviation |
|---|---:|---:|
| True ATE | 0.074285 | 0.000211 |
| Estimated ATE | 0.078459 | 0.008678 |
| ATE Bias | 0.004174 | 0.008500 |
| Absolute ATE Bias | 0.006164 | 0.006822 |
| MAE | 0.018969 | 0.002112 |
| RMSE | 0.023148 | 0.002122 |
| Effect Correlation | 0.617850 | 0.138233 |

**Interpretation**

The model slightly overestimated the average treatment effect across the five experiments. The mean absolute ATE bias was 0.006164.

The effect correlation ranged from 0.418135 to 0.804518, indicating variation in customer-level treatment-effect prediction across different holdout samples.

The results demonstrate that average treatment-effect estimation is reasonably consistent, although individual treatment-effect predictions remain sensitive to the validation split.

**Limitation:** The validation uses one synthetic dataset and five random seeds. Its findings should not be interpreted as proof of generalisation to real-world pricing data.

**Evaluation script:** `src/evaluation/validate_dml_against_truth.py`

**Individual results:** `reports/dml_truth_repeated_seed_results.csv`

**Summary report:** `reports/dml_truth_repeated_seed_summary.csv`


## 12. Automated Tests

Automated tests are included in:

- `tests/test_dynamic_pricing.py`
- `tests/test_compare_dml_estimators.py`

The tests cover dynamic-pricing functionality, Difference-in-Means baseline calculations, and DML evaluation metrics.

The previously recorded test result was:

**38 tests passed in 14.09 seconds.**

A subsequent verification run in the current Python 3.13 environment produced:

**38 tests passed in 6.34 seconds.**

Run the test suite from the repository root:

```powershell
python -m pytest -q
```

The test suite should be run again before final submission to confirm that it still passes after any subsequent code changes.

## 13. Limitations and Critical Analysis

### 13.1 Synthetic Data Limitations

The dynamic-pricing experiment uses synthetic customer data and a controlled purchase-probability formula.

Although this allows comparison against known simulation assumptions, it cannot fully represent real customer behaviour, market competition, inventory constraints, or operational costs.

### 13.2 Observational Retail Data

The Online Retail dataset is observational.

Price and quantity may be affected by product characteristics, promotions, seasonality, customer composition, and other confounding factors.

Therefore, the observed price-quantity relationships cannot automatically be interpreted as causal price effects.

### 13.3 Limitation 1 — Holdout ATE Bias and Repeated-Seed Sensitivity

The initial holdout evaluation showed that the LinearDML estimated ATE was higher than the synthetic reference ATE:

- True ATE: 0.074861.
- Estimated ATE: 0.092794.
- ATE bias: +0.017932 (approximately +1.79 percentage points).

To investigate whether this result was specific to one train/test partition, the Difference-in-Means baseline and both DML estimators were evaluated across five random seeds: 42, 7, 21, 35, and 99.

The repeated-seed evaluation produced the following mean absolute ATE bias:

| Estimator | Mean Absolute ATE Bias |
|---|---:|
| Difference-in-Means baseline | 0.006121 |
| LinearDML | 0.006120 |
| NonParamDML | 0.005975 |

The three estimators produced very similar mean absolute ATE bias. NonParamDML had the lowest average value, while LinearDML was effectively tied with the Difference-in-Means baseline.

LinearDML performed better than NonParamDML on individual treatment-effect prediction metrics, including MAE, RMSE, and effect correlation. Individual-effect metrics are not applicable to the Difference-in-Means baseline because it estimates only an aggregate treatment effect.

**Seed 42 investigation:** Seed 42 was a particularly sensitive partition. The raw treatment-group purchase-rate difference was approximately 9.07% in the training set and 3.72% in the holdout set. The estimated ATEs were:

- Difference-in-Means: 0.090660.
- LinearDML: 0.092794.
- NonParamDML: 0.090849.
- Synthetic reference ATE: 0.074861.

All three estimates were above the synthetic reference ATE on this split.

This suggests sensitivity to the train/test partition and variation in observed treatment-group outcomes. It does not establish overfitting or identify a definitive cause.

**Mitigation and further work:**

- Run additional seeds to strengthen the robustness assessment.
- Test alternative train/test partitions.
- Investigate treatment-outcome variation across partitions.
- Report uncertainty intervals where statistically appropriate.
- Evaluate the estimators under alternative synthetic data-generating scenarios.

**Limitation:** These findings are based on five evaluation seeds and a synthetic pricing dataset. They provide diagnostic evidence but are not sufficient to establish general estimator superiority or real-world pricing effectiveness.

### 13.4 Limitation 2 — Discount-Specific DML Accuracy and Uncertainty

A separate evaluation investigated how accurately LinearDML estimates the average treatment effect (ATE) for each tested discount relative to the 0% control group. This analysis is distinct from the overall comparison of LinearDML and NonParamDML reported in Section 11.

The evaluation used four treatment levels (5%, 10%, 15%, and 20%), five train/test split seeds (42, 7, 21, 35, and 99), and a 75%/25% split stratified by treatment assignment. Each holdout set contained 2,500 customers. LinearDML was fitted with statsmodels inference to obtain 95% ATE intervals.

**Repeated-seed results**

| Discount | Mean true ATE | Mean estimated ATE | Estimate SD | Mean bias | Mean absolute bias | Mean MAE | Mean RMSE | Observed CI coverage |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 5% | 0.027647 | 0.009520 | 0.008459 | -0.018127 | 0.018127 | 0.038168 | 0.046460 | 5/5 |
| 10% | 0.057656 | 0.059872 | 0.008990 | +0.002216 | 0.007450 | 0.029721 | 0.037043 | 5/5 |
| 15% | 0.089559 | 0.105017 | 0.016462 | +0.015457 | 0.018848 | 0.043248 | 0.052736 | 5/5 |
| 20% | 0.123613 | 0.135066 | 0.003993 | +0.011453 | 0.011453 | 0.024044 | 0.031343 | 5/5 |

ATE values and biases in this table are proportions; multiply by 100 to express them as percentage points. For example, a bias of 0.015457 corresponds to approximately +1.55 percentage points.

The 15% estimate varied most across the five splits (ATE standard deviation 0.016462) and had the largest mean absolute ATE bias (0.018848) among the four discount levels. The 5% estimate also showed meaningful underestimation (mean bias -0.018127). Therefore, the discrepancy is not limited to the 15% treatment level.

For the 15% discount, the seed-level estimated ATEs were 0.120653, 0.113216, 0.096697, 0.080189, and 0.114329. Four of the five estimates were above the corresponding synthetic reference effect, while one was below it. This indicates sensitivity to the selected split; it does not by itself establish overfitting or identify a single cause.

All five calculated 95% intervals contained the reference ATE for each discount in this evaluation. This is an observed result for five runs per discount, not evidence that the intervals have proven 95% coverage. A larger simulation study is required to assess interval coverage reliably.

**Nuisance-model and sample-size diagnostics**

The treatment model's ROC-AUC was approximately 0.500 for every discount. Because treatment assignment was randomized in the synthetic generator, a treatment-model score near 0.5 is expected and should not be interpreted as evidence of a failed treatment model.

| Discount | Outcome-model RMSE | Outcome-model R² | Treatment ROC-AUC |
|---|---:|---:|---:|
| 5% | 0.408579 | 0.046232 | 0.500 |
| 10% | 0.414323 | 0.044018 | 0.500 |
| 15% | 0.421426 | 0.045473 | 0.500 |
| 20% | 0.426260 | 0.052118 | 0.500 |

The outcome-model R² values were modest and similar across the four discount levels. The 15% outcome RMSE was somewhat higher, but its R² was not materially different from the other groups. The discount-specific treatment-arm sample sizes were also not smallest at 15%; therefore, the diagnostics do not support attributing the 15% discrepancy simply to a uniquely small treatment group.

**Interpretation and next steps**

These results provide a more detailed diagnostic of discount-specific ATE estimation than a single holdout split. They suggest that estimated effects can vary by discount level and train/test partition, and that average-effect accuracy and individual-effect prediction accuracy should be considered separately.

Further work should:

- Increase the number of evaluation seeds beyond five.
- Assess confidence-interval coverage over a substantially larger number of repeated simulations.
- Evaluate all three estimators across additional random seeds and alternative synthetic data-generating scenarios.
- Investigate both the 5% underestimation and the 15% overestimation.
- Report ATE bias, MAE, RMSE, estimate variation, and interval coverage together.

The discount-specific repeated-seed results are diagnostic evidence from a synthetic experiment. They do not establish real-world pricing effects or prove general estimator superiority.

### 13.5 Pricing-Policy Limitations

The 5% discount produced the highest expected profit among the five tested policies, but the improvement over no discount was only approximately 0.53%.

The comparison depends on the synthetic purchase-probability model and illustrative product-cost assumptions.

Additional validation is required before making any real-world pricing recommendation.

### 13.6 Generalisation and Reproducibility

The results are dependent on the selected datasets, modelling assumptions, and evaluation partitions.

The five-seed evaluation provides more evidence than a single holdout split, but additional seeds and alternative data-generating scenarios are needed to assess robustness more thoroughly.

The reported results should be reproduced from the repository before final submission.

## 14. Scientific Conclusion

The EconoCausal project demonstrates how causal inference, machine learning, and statistical analysis can support customer-level decision-making and pricing-policy evaluation.

The Hillstrom randomized marketing experiment provides evidence about the effects of email campaigns on customer visits and conversions. The Online Retail dataset provides an opportunity to explore historical product sales, price variations, and demand patterns. The synthetic pricing experiment allows treatment-effect estimators and pricing policies to be evaluated against known simulation assumptions. These three components address different analytical questions and should be interpreted separately.

In the synthetic pricing experiment, the mean absolute ATE bias across five evaluation seeds was 0.006121 for Difference-in-Means, 0.006120 for LinearDML, and 0.005975 for NonParamDML. These values are very close. NonParamDML had the lowest average ATE bias, while LinearDML was effectively tied with the aggregate baseline.

LinearDML performed better than NonParamDML on individual treatment-effect prediction metrics, including MAE, RMSE, and effect correlation. Individual-effect metrics are not applicable to Difference-in-Means because it estimates only an aggregate treatment effect.

The repeated-seed analysis also revealed sensitivity to the train/test partition, particularly for seed 42. These results are limited to five evaluation seeds and a synthetic pricing dataset; they do not establish general estimator superiority or real-world pricing effectiveness.

The synthetic dynamic-pricing comparison identified the 5% discount as the highest-profit option among the five tested policies. However, its advantage over the no-discount policy was approximately 0.53%. Since the experiment uses synthetic customer data and illustrative product-cost assumptions, this finding does not establish that a 5% discount is optimal for a real business.

The Online Retail analysis did not identify a statistically significant price-quantity relationship among the five selected products or in the pooled regression. Because the data are observational and the analysis has limited product-level monthly observations, these findings should be interpreted as exploratory rather than causal evidence about price elasticity.

Overall, the project provides a foundation for studying randomized marketing effects, observational product-demand patterns, synthetic causal estimation, and pricing-policy evaluation. Further work should focus on additional robustness checks, sensitivity analysis, realistic cost assumptions, and appropriate real-world validation.

The project demonstrates the importance of evaluating not only model predictions but also estimation error, experimental assumptions, reproducibility, and business relevance. Its current results are useful for research and educational purposes but should not be treated as validated real-world pricing recommendations.

## 15. Future Improvements and Development Roadmap

### Phase 1 — Current Project Foundation

- Complete the initial data analysis.
- Implement the synthetic pricing experiment.
- Implement and compare DML estimators.
- Evaluate candidate discount policies.
- Add automated tests and project documentation.

### Phase 2 — Robustness and Validation

- Extend the overall and discount-specific five-seed evaluations using additional random seeds and alternative data partitions.
- Investigate treatment-effect estimation stability.
- Extend uncertainty-interval evaluation and assess interval coverage over more repeated simulations.
- Test alternative synthetic data-generating scenarios.
- Improve the validation of individual treatment-effect estimates.

### Phase 3 — Pricing Model Improvements

- Explore multi-treatment discount estimation.
- Investigate customer-level pricing recommendations.
- Evaluate alternative pricing and profit assumptions.
- Consider inventory, competition, and operational constraints.
- Compare additional pricing policies.

### Phase 4 — Final Project Delivery

- Reproduce all reported results.
- Run the complete automated test suite.
- Review project structure and documentation.
- Prepare final visualisations and analysis reports.
- Verify GitHub repository completeness.
- Prepare the final project report and presentation.

## 16. Project Success Criteria

The project aims to demonstrate:

- Correct handling and preprocessing of multiple datasets.
- Appropriate separation of randomized, observational, and synthetic analyses.
- Application of causal inference methods.
- Comparison of DML estimators against a baseline.
- Evaluation using known synthetic reference effects.
- Repeated-seed robustness analysis.
- Comparison of pricing policies using expected profit.
- Reusable Python code and automated testing.
- Clear documentation of assumptions, results, and limitations.
- Reproducible project execution.

## 17. Team Note

This project is being developed as part of the Infotact internship programme.

The work combines data analysis, machine learning, causal inference, and business-oriented pricing evaluation.

The repository is maintained collaboratively, with development changes tracked through Git and GitHub.

**Repository:** [EconoCausal-Dynamic-Pricing](https://github.com/fahmaparveen3-arch/EconoCausal-Dynamic-Pricing)

**Development branch:** `Hiba`

---

**Project status:** The project has a working analytical foundation, recorded validation results, pricing-policy comparisons, and automated tests. Both exploratory notebooks have been run successfully in the current development environment, and the automated test suite has passed with 38 tests. Final reproducibility checks, integration review, and submission-quality verification remain necessary before claiming full project completion.