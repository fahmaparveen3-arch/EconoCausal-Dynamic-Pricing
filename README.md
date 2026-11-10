# EconoCausal — Causal Inference and Dynamic Pricing

An applied data science project combining causal inference, machine learning, customer analytics, and pricing-policy evaluation.

## 1. Project Overview

EconoCausal investigates how causal inference and machine learning can support customer-level treatment-effect estimation and dynamic pricing decisions.

The project combines three datasets:

- **Hillstrom Email Marketing Dataset:** Used to study the causal effect of email marketing campaigns and explore customer uplift.
- **UCI Online Retail Dataset:** Used for observational retail sales, product-price, and demand analysis.
- **Synthetic Dynamic-Pricing Dataset:** Used to evaluate discount-specific causal effects, validate Double Machine Learning (DML) models against known ground truth, and compare pricing policies.

The project uses Python, statistical analysis, machine learning, and causal inference techniques to examine treatment effects and pricing outcomes.

## 2. Project Objectives

The main objectives are:

1. Analyse the impact of email marketing campaigns using randomized experimental data.
2. Explore customer-level treatment effects and uplift modelling.
3. Develop a synthetic pricing dataset with known causal effects.
4. Apply Double Machine Learning to estimate discount-specific treatment effects.
5. Validate causal estimates against known synthetic ground truth.
6. Evaluate model performance across multiple random seeds and validation settings.
7. Compare pricing policies using expected revenue and expected profit.
8. Explore product-price and sales relationships using real-world retail data.
9. Build a reproducible and testable causal-inference workflow.

## 3. Technology Stack

| Area | Tools and Libraries |
|---|---|
| Programming language | Python 3.13 |
| Data manipulation | Pandas, NumPy |
| Data visualisation | Matplotlib, Seaborn |
| Machine learning | Scikit-learn |
| Causal inference | EconML |
| Statistical analysis | SciPy, Statsmodels |
| Notebook environment | Jupyter Notebook |
| Excel file handling | OpenPyXL |
| Automated testing | Pytest |
| Development environment | VS Code |
| Version control | Git and GitHub |
| Backend | FastAPI |
| Frontend | Next.js |

## 4. Project Structure

```text
EconoCausal-Dynamic-Pricing/
│
├── backend/
│   └── main.py
│
├── frontend/
│   └── src/
│       └── app/
│           └── page.tsx
│
├── data/
│   ├── hillstrom.csv
│   ├── synthetic_pricing.csv
│   ├── prepared_pricing.csv
│   ├── online+retail/
│   └── processed/
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
│   ├── evaluation/
│   │   ├── compare_discount_causal_effects.py
│   │   ├── compare_dml_estimators.py
│   │   ├── compare_pricing_policies.py
│   │   ├── evaluate_pricing_profit.py
│   │   ├── evaluate_uplift.py
│   │   ├── validate_dml_against_truth.py
│   │   ├── validate_dml_holdout.py
│   │   ├── validate_dml_model_configurations.py
│   │   ├── validate_dml_repeated_seeds.py
│   │   ├── validate_dml_repeated_split_ratios.py
│   │   └── validate_dml_split_ratios.py
│   │
│   ├── models/
│   │   ├── train_dml.py
│   │   └── train_uplift.py
│   │
│   └── pricing/
│       └── dynamic_pricing.py
│
├── reports/
│   ├── discount_causal_effect_comparison.csv
│   ├── dml_customer_effects.csv
│   ├── dml_estimator_comparison.csv
│   ├── dml_estimator_repeated_seed_results.csv
│   ├── dml_estimator_repeated_seed_summary.csv
│   ├── dml_holdout_validation.csv
│   ├── dml_model_configuration_results.csv
│   ├── dml_model_configuration_summary.csv
│   ├── dml_repeated_seed_80_20_results.csv
│   ├── dml_repeated_seed_80_20_summary.csv
│   ├── dml_repeated_split_ratios_results.csv
│   ├── dml_repeated_split_ratios_summary.csv
│   ├── dml_truth_holdout_validation.csv
│   ├── dml_truth_repeated_seed_results.csv
│   ├── dml_truth_repeated_seed_summary.csv
│   ├── dml_truth_validation.csv
│   ├── dml_split_ratio_validation.csv
│   ├── pricing_policy_comparison.csv
│   └── pricing_profit_evaluation.csv
│
├── tests/
│   ├── test_compare_dml_estimators.py
│   ├── test_discount_causal_effects.py
│   ├── test_dynamic_pricing.py
│   └── test_train_dml.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

**Data and generated files:** Some local datasets and generated outputs are intentionally excluded from Git through `.gitignore`. In particular, the local Hillstrom CSV, raw Online Retail files, processed files, and prepared pricing dataset are not necessarily included in a fresh clone. The tracked synthetic pricing dataset and report files are maintained separately.

**Historical reports:** `dml_estimator_comparison.csv` and `dml_truth_holdout_validation.csv` are retained historical outputs. They are not used as the latest validation results documented in Section 11.

## 5. Datasets

### 5.1 Hillstrom Email Marketing Dataset

The Hillstrom dataset contains 64,000 customers and 12 columns. It originates from a randomized email marketing experiment and includes three groups:

- Mens E-Mail
- Womens E-Mail
- No E-Mail

The dataset includes customer characteristics, campaign assignment, website visits, conversions, and spending.

The local dataset is expected at:

```text
data/hillstrom.csv
```

The project uses this dataset to compare email campaign outcomes and investigate customer uplift.

**Data source:** A publicly accessible mirror of the Hillstrom dataset is used:

[Hillstrom dataset CSV mirror](https://raw.githubusercontent.com/W-Tran/uplift-modelling/refs/heads/master/data/hillstrom/Kevin_Hillstrom_MineThatData_E-MailAnalytics_DataMiningChallenge_2008.03.20.csv)

The linked file is a third-party mirror, not the original publisher's website.

### 5.2 UCI Online Retail Dataset

The Online Retail dataset is obtained from the UCI Machine Learning Repository.

It contains transactional records from a UK-based online retailer between December 2010 and December 2011.

The dataset includes:

- Invoice number
- Product stock code
- Product description
- Quantity
- Invoice date
- Unit price
- Customer ID
- Country

**Official source:** [UCI Online Retail Dataset](https://archive.ics.uci.edu/dataset/352/online+retail)

The raw Excel file is expected at:

```text
data/online+retail/Online Retail.xlsx
```

This is observational transaction data. Relationships found in this dataset should not be interpreted as causal effects.

### 5.3 Synthetic Dynamic-Pricing Dataset

A synthetic customer-level dataset is generated to study discount-based pricing decisions.

It contains 10,000 customers and 14 columns.

The dataset includes customer characteristics, treatment assignment, discount information, purchase outcomes, and pricing-related variables.

A known ground-truth treatment effect is incorporated into the synthetic data-generation process. This makes it possible to compare estimated treatment effects with the reference causal effects.

The generator uses a fixed default random seed of 42 to support reproducibility.

The tracked dataset is:

```text
data/synthetic_pricing.csv
```

The prepared dataset is generated locally:

```text
data/prepared_pricing.csv
```

The prepared file is excluded from Git.

## 6. Data Preprocessing

### 6.1 Hillstrom Data

The Hillstrom dataset is used for randomized campaign analysis.

The analysis includes:

- Checking the dataset dimensions and column types.
- Examining missing values and data quality.
- Analysing the distribution of treatment groups.
- Comparing campaign conversion and visit rates.
- Preparing customer characteristics for modelling.
- Separating treatment and control groups for uplift analysis.

The primary campaign comparisons are Mens E-Mail versus No E-Mail and Womens E-Mail versus No E-Mail.

### 6.2 Online Retail Data

The Online Retail preprocessing workflow examines the original transaction data and separates valid product sales from records that should be audited or excluded.

| Processing category | Records |
|---|---:|
| Original dataset | 541,909 |
| Cleaned dataset | 524,110 |
| Product-sales dataset | 521,755 |
| Excluded records | 1,176 |

The excluded-record count is a separate audit category. It should not be treated as another sequential processing stage to add to the cleaned and product-sales counts.

Additional audit findings:

- Non-product audit records: 2,355.
- Returns and cancellations: 10,587.
- Excluded records: 1,176.
- Fully reversed audit records: 1,536.
- Product-sales dataset shape: 521,755 rows and 9 columns.
- Duplicate records in the final product-sales dataset: 0.
- Invalid quantity records in the final product-sales dataset: 0.
- Invalid unit-price records in the final product-sales dataset: 0.
- Invalid invoice-date records in the final product-sales dataset: 0.
- Revenue consistency: revenue equals quantity multiplied by unit price.
- Missing CustomerID values: 131,420.

Because many records do not contain a CustomerID, customer-level analysis is limited. The project therefore focuses on transaction-level and product-level analysis where appropriate.

### 6.3 Synthetic Pricing Data

The synthetic pricing dataset is generated and prepared through separate modules.

The preparation workflow includes:

- Loading the generated pricing dataset.
- Checking required columns.
- Validating customer identifiers.
- Checking treatment and outcome variables.
- Checking discount values.
- Preparing the data for causal estimation.
- Validating missing values and numerical ranges.

Verified prepared dataset:

| Check | Result |
|---|---:|
| Rows | 10,000 |
| Columns | 14 |
| Missing values | 0 |
| Duplicate customer IDs | 0 |
| Control customers | 5,003 |
| Treatment customers | 4,997 |
| Discount rules valid | True |

## 7. Methodology

### 7.1 Hillstrom Marketing Causal Analysis

The randomized Hillstrom experiment is used to estimate the impact of email marketing campaigns.

The main comparisons are:

- Mens E-Mail versus No E-Mail.
- Womens E-Mail versus No E-Mail.

The analysis examines conversion rates, visit rates, spending, statistical significance, and confidence intervals.

A baseline conversion prediction model and a T-learner approach are also used to explore customer-level uplift.

### 7.2 Causal Machine Learning

Double Machine Learning is applied to estimate customer-level treatment effects in the synthetic pricing dataset.

The DML workflow includes:

1. Data validation.
2. Feature preparation.
3. Treatment and outcome definition.
4. Model fitting.
5. Customer-level treatment-effect estimation.
6. Holdout evaluation.
7. Comparison with known synthetic ground truth.

The implementation uses EconML and machine-learning models from Scikit-learn.

The project also compares LinearDML, NonParamDML with Gradient Boosting, and a Difference-in-Means baseline.

### 7.3 Synthetic Ground-Truth Validation

The synthetic dataset contains known treatment effects.

This allows the estimated treatment effects to be evaluated using:

- Average Treatment Effect (ATE).
- Estimation bias.
- Mean Absolute Error (MAE).
- Root Mean Squared Error (RMSE).
- Correlation between estimated and true customer-level effects.
- Confidence-interval coverage.

The project uses holdout evaluation and repeated random seeds to examine how stable the estimates are under different data splits.

### 7.4 Dynamic Pricing and Expected Profit

The project evaluates multiple discount policies.

The pricing analysis considers:

- Discount rate.
- Expected purchase rate.
- Expected revenue per customer.
- Expected profit per customer.
- Total expected revenue.
- Total expected profit.

The purpose is to compare the tested pricing policies under the assumptions of the synthetic dataset.

### 7.5 Repeated-Seed DML Evaluation

Repeated-seed evaluation is used to examine the stability of causal estimates.

Five random seeds are used:

```text
42, 7, 21, 35, 99
```

Each evaluation uses a stratified 75/25 train-test split.

The same holdout partitions are used for the estimators being compared within each seed.

Both `compare_dml_estimators.py` and `validate_dml_against_truth.py` calculate the reference ATE using the empirical proportions of the four discount levels among treated customers.

Reference ATE values can differ across evaluation runs because the data splits, seeds, and evaluation designs may differ. Results should therefore be compared only when they come from compatible evaluation settings.

### 7.6 Online Retail Price and Demand Analysis

The Online Retail dataset is used to examine selected products over time.

The analysis includes:

- Selecting products with sufficient transaction history.
- Aggregating sales by month.
- Calculating weighted average prices.
- Examining monthly sales patterns.
- Exploring correlations between price and quantity.
- Fitting an exploratory regression model.

The analysis is observational. It does not establish that price changes caused changes in demand.

### 7.7 Online Retail Exploratory Results

Five selected products were analysed over 13 months each, producing 65 monthly observations.

The Pearson correlations between monthly weighted average price and quantity were:

| Product | Correlation (r) | p-value |
|---|---:|---:|
| 20725 Lunch Bag Red Retrospot | -0.3388 | 0.2575 |
| 22423 Regency Cake Stand 3 Tier | +0.1956 | 0.5219 |
| 47566 Party Bunting | -0.0916 | 0.7660 |
| 85099B Jumbo Bag Red Retrospot | +0.1329 | 0.6652 |
| 85123A White Hanging Heart T-Light Holder | +0.0809 | 0.7928 |

None of the five product-level correlations is statistically significant at the 5% level.

The exploratory regression using 65 observations produced:

| Statistic | Result |
|---|---:|
| Price coefficient | 0.3691 |
| Standard error | 1.2321 |
| t-statistic | 0.2995 |
| p-value | 0.7658 |
| Residual degrees of freedom | 47 |

The price coefficient is not statistically significant at the 5% level.

These results should be interpreted cautiously because:

- Only 13 monthly observations are available per product.
- Monthly weighted average prices can change because of transaction and quantity mix, not necessarily because the actual listed price changed.
- The data are observational.
- Potential confounding, endogeneity, and time-series dependence may affect the estimates.

Therefore, the results do not establish causal price elasticity.

## 8. Setup and Installation

### 8.1 Requirements

The project uses Python 3.13 and the dependencies listed in `requirements.txt`.

Git is required to clone the repository.

### 8.2 Clone Repository

```bash
git clone https://github.com/fahmaparveen3-arch/EconoCausal-Dynamic-Pricing.git
cd EconoCausal-Dynamic-Pricing
```

### 8.3 Create Virtual Environment

On Windows, using the Python launcher:

```powershell
py -3.13 -m venv .venv
```

Alternatively, use an installed Python 3.13 executable.

### 8.4 Activate Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 8.5 Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The project's development environment was verified using Python 3.13.16. All pinned dependencies installed successfully, and `pip check` reported no broken requirements.

## 9. Running the Project

Run Python commands from the repository root.

### 9.1 Generate Synthetic Pricing Data

```bash
python -m src.data_processing.generate_synthetic_pricing_data
```

This generates the synthetic pricing dataset.

**Important:** The generator writes to `data/synthetic_pricing.csv`, which is tracked by Git. Running it may overwrite the existing dataset. Review the generated changes with `git diff` before staging or committing.

### 9.2 Prepare Synthetic Pricing Data

```bash
python -m src.data_processing.prepare_pricing_data
```

This prepares the synthetic pricing data and writes the locally generated `data/prepared_pricing.csv` file.

The prepared dataset is excluded from Git.

### 9.3 Compare Pricing Policies

```bash
python -m src.evaluation.compare_pricing_policies
```

This compares the tested discount policies and writes:

```text
reports/pricing_policy_comparison.csv
```

**Important:** This command overwrites the existing report. Review the results before committing any changes.

### 9.4 Run Automated Tests

```bash
python -m pytest -v
```

The verified test suite completed with 38 passing tests.

### 9.5 Run Repeated-Seed DML Comparison

```bash
python -m src.evaluation.compare_dml_estimators
```

This evaluates the DML estimators over five random seeds and generates repeated-seed result and summary reports.

The script calculates its reference average treatment effect using the empirical proportions of discount levels among treated customers.

### 9.6 Preprocess Online Retail Data

```bash
python -m src.data_processing.preprocess_online_retail
```

This processes the raw Online Retail dataset and generates the required local processed files.

The raw and processed Online Retail data directories are excluded from Git.

### 9.7 Hillstrom Analysis

Open the following notebook in Jupyter Notebook:

```text
notebooks/01_hillstrom_eda.ipynb
```

The local Hillstrom dataset must be available at:

```text
data/hillstrom.csv
```

### 9.8 Online Retail Analysis

Open the following notebook in Jupyter Notebook:

```text
notebooks/02_online_retail_eda.ipynb
```

The raw Online Retail Excel dataset must be available at:

```text
data/online+retail/Online Retail.xlsx
```

### 9.9 Run the Dashboard

The project includes a FastAPI backend and a Next.js frontend.

**Start the backend:**

From the repository root, activate the Python virtual environment and run:

```bash
python -m uvicorn backend.main:app --reload
```

**Start the frontend:**

Open a separate terminal and navigate to the frontend directory:

```bash
cd frontend
npm install
npm run dev
```

Open the local frontend address displayed in the terminal. The backend API runs separately and provides the data used by the dashboard.

## 10. Pricing-Policy Results

The synthetic pricing-policy comparison evaluates five discount rates.

| Discount rate | Expected purchase rate | Expected revenue per customer | Expected profit per customer | Total expected revenue | Total expected profit |
|---:|---:|---:|---:|---:|---:|
| 0% | 0.2078 | 76.16 | 33.24 | 761,609.82 | 332,435.25 |
| 5% | 0.2354 | 82.17 | 33.42 | 821,743.83 | 334,186.01 |
| 10% | 0.2653 | 87.95 | 32.85 | 879,531.41 | 328,546.76 |
| 15% | 0.2972 | 93.33 | 31.41 | 933,261.15 | 314,052.64 |
| 20% | 0.3311 | 98.11 | 28.93 | 981,100.87 | 289,266.88 |

The 5% discount policy produced the highest expected profit per customer among the five tested policies.

- 5% discount: 33.42 expected profit per customer.
- No discount: 33.24 expected profit per customer.
- The 5% discount policy produced approximately 0.53% higher expected profit than the no-discount policy.

The 20% discount produced the highest expected revenue but the lowest expected profit per customer among the tested policies.

These results depend on the assumptions and ground-truth relationships built into the synthetic dataset. The 5% discount is the best-performing policy among those tested, not a proven optimal discount for a real business.

## 11. DML Validation Results

### 11.1 Full-Dataset Ground-Truth Validation

The full-dataset validation compared estimated customer treatment effects with the known synthetic effects.

| Metric | Result |
|---|---:|
| True ATE | 0.074463 |
| Estimated ATE | 0.079521 |
| Bias | +0.005058 |
| MAE | 0.016636 |
| RMSE | 0.020166 |

The estimated ATE is slightly higher than the reference ATE.

### 11.2 Holdout Validation

The holdout evaluation used a 75/25 split, producing 2,500 test customers.

| Metric | Result |
|---|---:|
| Holdout customers | 2,500 |
| True ATE | 0.074642 |
| Estimated ATE | 0.092794 |
| Bias | +0.018151 |
| MAE | 0.021127 |
| RMSE | 0.024365 |

The holdout estimate is higher than the reference ATE. This difference demonstrates why a single train-test split should not be treated as sufficient evidence of model stability.

### 11.3 Repeated-Seed Estimator Comparison

Five seeds were used to compare Difference-in-Means, LinearDML, and NonParamDML with Gradient Boosting.

The comparison uses empirical discount-level proportions among treated customers to calculate the reference ATE. Each estimator was evaluated over five random seeds, with 2,500 holdout customers per run.

| Metric | Difference-in-Means | LinearDML | NonParamDML |
|---|---:|---:|---:|
| Mean estimated ATE | 0.077594 | 0.078459 | 0.078441 |
| Mean bias | +0.003502 | +0.004367 | +0.004350 |
| Mean absolute bias | 0.005759 | 0.005758 | 0.005613 |
| Bias standard deviation | 0.007013 | 0.007251 | 0.006600 |

Additional individual-effect metrics:

| Metric | Difference-in-Means | LinearDML | NonParamDML |
|---|---:|---:|---:|
| Mean MAE | N/A | 0.018630 | 0.035615 |
| Mean RMSE | N/A | 0.022803 | 0.050003 |
| Mean effect correlation | N/A | 0.617875 | 0.231011 |

The Difference-in-Means baseline estimates the overall treatment effect but does not provide the individual treatment-effect predictions required for the individual-effect MAE, RMSE, and correlation metrics.

In these five runs, LinearDML produced lower mean individual-effect MAE and RMSE than NonParamDML. These results describe the tested configuration and seeds; they do not establish universal estimator superiority.

### 11.4 Holdout Seed 42 Investigation

The seed 42 holdout evaluation produced:

| Estimator | True ATE | Estimated ATE | Bias | MAE | RMSE |
|---|---:|---:|---:|---:|---:|
| Difference-in-Means | 0.076858 | 0.090660 | +0.013802 | N/A | N/A |
| LinearDML | 0.076858 | 0.092794 | +0.015936 | 0.019827 | 0.022772 |
| NonParamDML | 0.076858 | 0.090849 | +0.013990 | 0.034340 | 0.047038 |

The investigation also examined differences between the training and test samples. The seed 42 result illustrates how sampling variation can affect holdout estimates.

It should be interpreted alongside the repeated-seed results rather than as an isolated measure of model performance.

### 11.5 DML Model Configuration Comparison

Three Gradient Boosting configurations were evaluated over five random seeds. Each run used 8,000 training customers and 2,000 holdout customers.

| Configuration | Trees | Minimum samples per leaf | Mean MAE | Mean RMSE | Mean effect correlation | Mean absolute ATE bias |
|---|---:|---:|---:|---:|---:|---:|
| Baseline | 100 | 20 | 0.018132 | 0.022214 | 0.587706 | 0.003982 |
| Config A | 100 | 10 | 0.018626 | 0.022732 | 0.585795 | 0.003745 |
| Config B | 200 | 20 | 0.018033 | 0.022106 | 0.590228 | 0.004217 |

Config B produced marginally lower mean MAE and RMSE and slightly higher effect correlation. However, the differences were small, and Config A had the lowest mean absolute ATE bias. The baseline remains a reasonable choice because of its simpler configuration.

## 12. Automated Tests

The project contains four automated test files:

```text
tests/
├── test_compare_dml_estimators.py
├── test_discount_causal_effects.py
├── test_dynamic_pricing.py
└── test_train_dml.py
```

The complete test suite was executed using:

```bash
python -m pytest -v
```

Test result:

```text
38 passed in 13.87s
```

All 38 tests passed in the verified development environment.

Additional environment checks:

- Python version: 3.13.16.
- Required package imports: successful.
- Dependency consistency: `pip check` reported no broken requirements.

## 13. Limitations and Critical Analysis

### 13.1 Hillstrom Dataset Limitations

The Hillstrom dataset comes from a randomized marketing experiment, which supports causal comparisons of the campaign groups.

However:

- The findings relate to the specific experiment and customer population.
- Campaign effects may differ across customer segments.
- Customer-level uplift estimates are harder to validate than overall treatment effects.
- A high-performing uplift ranking should not be assumed without sufficient validation.

### 13.2 Uplift Model Limitations

The baseline conversion model achieved:

| Metric | Result |
|---|---:|
| ROC-AUC | 0.5490 |
| PR-AUC | 0.0103 |

The T-learner produced a mean predicted uplift of approximately 0.632 percentage points.

The estimated Qini value was 0.8665, and the estimated incremental conversions were approximately 35.707.

For the top 20% of customers selected by predicted uplift, the observed treatment conversion rate was 1.531%, compared with 0.217% in the control group, giving an observed difference of approximately 1.313 percentage points.

The observed test-set ATE was approximately 0.832 percentage points, compared with the predicted mean uplift of approximately 0.632 percentage points.

These are exploratory results. Predicted uplift and observed treatment-control differences are not identical quantities, and the results should not be interpreted as guaranteed campaign gains.

Bootstrap comparisons did not establish statistically supported superiority of the tested uplift models:

| Comparison | Estimated difference | 95% confidence interval |
|---|---:|---:|
| HGB versus Random Forest Qini | 1.4925 | [-3.2586, 6.4940] |

The confidence interval includes zero. Therefore, the available evidence does not establish that HGB outperforms Random Forest.

### 13.3 DML Holdout and Repeated-Seed Limitations

The initial holdout estimate showed a positive difference between estimated and true ATE.

Repeated-seed evaluation provides additional evidence about model stability, but five random seeds are still a limited sample of possible data splits.

Results can vary depending on:

- The random seed.
- Training and test sample composition.
- Treatment and outcome model configurations.
- The distribution of discount levels.
- The definition used to calculate the reference ATE.

The project therefore reports both single-split and repeated-seed results instead of relying on one estimate.

### 13.4 Discount-Specific LinearDML Validation

Discount-specific validation compared the estimated causal effects with the known synthetic effects over five seeds.

| Discount | Mean true ATE | Mean estimated ATE | Estimate SD | Mean bias | Mean absolute bias | Mean MAE | Mean RMSE | CI coverage |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 5% | 0.027647 | 0.009520 | 0.008459 | -0.018127 | 0.018127 | 0.038168 | 0.046460 | 5/5 |
| 10% | 0.057656 | 0.059872 | 0.008990 | +0.002216 | 0.007450 | 0.029721 | 0.037043 | 5/5 |
| 15% | 0.089559 | 0.105017 | 0.016462 | +0.015457 | 0.018848 | 0.043248 | 0.052736 | 5/5 |
| 20% | 0.123613 | 0.135066 | 0.003993 | +0.011453 | 0.011453 | 0.024044 | 0.031343 | 5/5 |

The results indicate:

- The 5% discount effect was underestimated on average.
- The 10% discount estimate was closest to its reference ATE on average.
- The 15% discount had the highest mean absolute ATE bias and the largest estimate standard deviation.
- The 20% discount estimate was higher than its reference ATE on average.

All five calculated confidence intervals contained the corresponding reference ATE for each discount level.

However, five runs are not sufficient to establish that the intervals achieve their nominal 95% coverage in general.

The treatment-model ROC-AUC was approximately 0.5. This is consistent with the randomized treatment assignment in the synthetic data and should not automatically be interpreted as model failure.

### 13.5 Dynamic-Pricing Limitations

The 5% discount produced the highest expected profit among the five tested pricing policies.

However:

- The pricing data are synthetic.
- The result depends on the assumptions used to generate customer responses.
- Only the tested discount policies are compared.
- Real businesses may have different costs, customer behaviour, demand patterns, and competitive conditions.

Therefore, the result should not be interpreted as a universal pricing recommendation.

### 13.6 Repeated-Seed Evaluation Limitations

The five-seed evaluation is more informative than relying on a single random split.

However, additional seeds, model configurations, sample sizes, and treatment scenarios would provide stronger evidence about generalisation and stability.

### 13.7 Online Retail Limitations

The Online Retail dataset is observational.

The product-level correlations and regression results do not establish causal price elasticity.

Other factors, such as seasonality, product popularity, promotions, stock availability, and transaction composition, may influence observed sales and prices.

The limited monthly observations also restrict the strength of statistical conclusions.

## 14. Scientific Conclusion

EconoCausal demonstrates how causal inference and machine learning can be applied to customer analytics and dynamic pricing.

The Hillstrom experiment supports the analysis of email marketing treatment effects and provides an opportunity to explore customer uplift.

The synthetic pricing dataset allows DML estimates to be compared against known ground-truth treatment effects. Holdout and repeated-seed evaluations show why causal estimates should be examined across multiple data splits.

The pricing-policy comparison identifies the 5% discount as the highest-profit option among the five tested synthetic policies. This finding is specific to the assumptions of the generated dataset and does not establish a real-world optimal discount.

The Online Retail analysis provides exploratory evidence about product prices and sales. None of the five examined product-level price-quantity correlations was statistically significant at the 5% level, and the observational data do not support causal conclusions.

Overall, the project demonstrates a reproducible workflow for causal analysis, model validation, and pricing-policy evaluation while acknowledging the limitations of synthetic and observational data.

## 15. Future Improvements and Development Roadmap

Potential future improvements include:

1. Evaluate DML models across more random seeds.
2. Test additional treatment and outcome model configurations.
3. Examine larger and more diverse synthetic pricing scenarios.
4. Explore alternative causal estimators.
5. Improve customer-level uplift evaluation.
6. Investigate additional uncertainty-estimation methods.
7. Incorporate more realistic pricing constraints and business costs.
8. Explore stronger time-series methods for retail demand analysis.
9. Evaluate the methodology using real-world randomized pricing experiments where available.
10. Improve automated reporting and reproducibility checks.

## 16. Project Success Criteria

The project aims to meet the following criteria:

- Integrate multiple datasets for customer and retail analysis.
- Perform exploratory data analysis and data preprocessing.
- Estimate treatment effects using causal inference methods.
- Compare causal estimates against known synthetic ground truth.
- Evaluate model performance using holdout and repeated-seed validation.
- Compare discount policies using expected revenue and expected profit.
- Maintain modular Python source code.
- Provide automated tests for key project functionality.
- Document data sources, methods, results, and limitations.
- Maintain a reproducible project structure and GitHub repository.

## 17. Team Note

This project was developed as part of the EconoCausal Dynamic Pricing internship project.

The work combines exploratory data analysis, synthetic data generation, causal machine learning, pricing-policy evaluation, validation, and documentation.

The project uses both randomized experimental data and observational retail data, alongside synthetic data with known causal effects. Findings are interpreted according to the strengths and limitations of each data source.

**Project status:** Core integration, reproducibility checks, and the automated test suite have been completed in the current development environment. Final repository review and submission preparation remain.