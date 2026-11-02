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

The repository is organised into data-processing, pricing, evaluation, testing, notebook, and reporting components.

```text
EconoCausal-Dynamic-Pricing/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   └── hillstrom_eda.ipynb
│
├── src/
│   ├── data_processing/
│   │   └── generate_synthetic_pricing_data.py
│   │
│   ├── pricing/
│   │   └── dynamic_pricing.py
│   │
│   └── evaluation/
│       ├── compare_dml_estimators.py
│       └── compare_pricing_policies.py
│
├── reports/
│   ├── dml_customer_effects.csv
│   ├── dml_estimator_comparison.csv
│   ├── dml_estimator_repeated_seed_results.csv
│   ├── dml_estimator_repeated_seed_summary.csv
│   ├── dml_holdout_validation.csv
│   ├── dml_truth_validation.csv
│   ├── pricing_policy_comparison.csv
│   └── pricing_profit_evaluation.csv
│
├── tests/
│   └── test_dynamic_pricing.py
│
├── README.md
└── requirements.txt
```

This tree shows the principal project files and reports. Additional files, notebooks, and data files may also exist in the repository.

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

Earlier analysis recorded the following results:

| Comparison or Metric | Recorded Result |
|---|---:|
| Men's email vs. no email — conversion effect | +0.681 percentage points |
| Women's email vs. no email — conversion effect | +0.311 percentage points |
| Uplift model ROC-AUC | 0.5490 |
| Uplift model PR-AUC | 0.0103 |
| Reported predicted uplift | 0.632 percentage points |

These are results from the earlier marketing-analysis stage and should be reproduced from the project files before final submission.

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

The recorded preprocessing counts were:

| Preprocessing Stage | Rows |
|---|---:|
| Original dataset | 541,909 |
| After duplicate removal | 536,641 |
| Cancellation records | 9,251 |
| Fully reversed audit records | 1,206 |
| Fully reversed original sales removed | 603 |
| Return records | 1,336 |
| Invalid sales excluded | 1,176 |
| Clean sales records | 524,275 |
| Product sales records | 521,917 |
| Non-product records | 2,358 |

The cleaned product-sales dataset was checked for duplicate records, missing product descriptions, invalid quantities, invalid prices, and revenue inconsistencies.

Recorded validation results:

- Product sales records: 521,917.
- Duplicate rows: 0.
- Missing product descriptions: 0.
- Invalid quantity or price records: 0.
- Revenue discrepancies: 0.
- CustomerID missingness: approximately 25.2%.

### 6.3 Synthetic Pricing Data

The synthetic pricing data was generated using a controlled probability model.

The generator uses customer characteristics and discount rates to calculate purchase probabilities. A binary purchase outcome is then generated from those probabilities.

Treatment assignment is randomized, and treated customers receive one of the tested positive discount levels.

This controlled design allows the project to compare estimated effects with reference effects calculated from the simulation.

## 7. Methodology

### 7.1 Hillstrom Marketing Causal Analysis

The Hillstrom analysis investigates whether email marketing interventions affect customer visits and conversions.

The principal comparison uses:

- Treatment group: Men's E-Mail.
- Control group: No E-Mail.
- Outcome: Customer conversion.

The analysis compares conversion rates and estimates the difference between the treatment and control groups.

The Women's E-Mail group is also examined separately.

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

To investigate sensitivity to train/test partitions, both DML estimators were evaluated across five random seeds:

`42, 7, 21, 35, 99`

The dataset was divided using a 75% training and 25% holdout split, stratified by treatment assignment.

Each run used:

- 7,500 training customers.
- 2,500 holdout customers.

The same evaluation seeds and corresponding splits were used for both estimators.

### 7.6 Online Retail Price and Demand Analysis

The Online Retail analysis explores product-level relationships between unit price and quantity sold.

It includes product-level correlation analysis and a pooled regression.

The analysis is exploratory because the dataset is observational and product prices may be influenced by factors other than demand.

### 7.7 Online Retail Exploratory Results

The recorded product-level correlation results were:

| Product | Price-Quantity Correlation | p-value |
|---|---:|---:|
| Lunch Bag Red Retrospot | -0.3388 | 0.2575 |
| Regency Cake Stand | +0.1984 | 0.5158 |
| Party Bunting | -0.0916 | 0.7660 |
| Jumbo Bag | +0.1192 | 0.6982 |
| White Hanging Heart | +0.0815 | 0.7911 |

The recorded pooled regression results were:

| Metric | Result |
|---|---:|
| Price coefficient | +0.3416 |
| Standard error | 1.2339 |
| t-statistic | 0.2769 |
| p-value | 0.7831 |
| Observations | 65 |
| Residual degrees of freedom | 47 |

The analysis did not identify a statistically significant price-quantity relationship among the five selected products or in the pooled regression.

These results should be treated as exploratory findings, not causal estimates of price elasticity.

## 8. Setup and Installation

### 8.1 Clone the Repository

```bash
git clone https://github.com/fahmaparveen3-arch/EconoCausal-Dynamic-Pricing.git
```

### 8.2 Move into the Project Directory

```bash
cd EconoCausal-Dynamic-Pricing
```

### 8.3 Create a Virtual Environment

```bash
python -m venv .venv
```

### 8.4 Activate the Virtual Environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 8.5 Install Dependencies

```bash
pip install -r requirements.txt
```

The project was also developed and tested in a Python 3.13.16 environment named `.venv313`.

## 9. Running the Project

Run project commands from the repository root.

### 9.1 Generate Synthetic Pricing Data

```bash
python -m src.data_processing.generate_synthetic_pricing_data
```

### 9.2 Compare Pricing Policies

```bash
python -m src.evaluation.compare_pricing_policies
```

### 9.3 Run Automated Tests

```bash
pytest
```

### 9.4 Compare DML Estimators Across Repeated Seeds

Run from the project root:

```bash
python -m src.evaluation.compare_dml_estimators
```

Outputs:

- `reports/dml_estimator_repeated_seed_results.csv` — detailed results for each estimator and random seed.
- `reports/dml_estimator_repeated_seed_summary.csv` — aggregated performance metrics across the five seeds.

The single-split estimator comparison report contains previously generated results and is not regenerated by the current repeated-seed script.

### 9.5 Online Retail Data Preprocessing

The Online Retail preprocessing workflow is part of the project's data-preparation stage.

The exact script name and execution command should be documented here after verifying the preprocessing file in the repository.

### 9.6 Run Hillstrom Analysis

The Hillstrom exploratory analysis is available in the project notebook:

`notebooks/hillstrom_eda.ipynb`

Open and run the notebook in Jupyter or VS Code after placing the dataset in the expected data location.

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

Both DML estimators were evaluated across five random seeds.

The recorded mean results were:

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
| Difference-in-Means baseline | 0.016959 |
| LinearDML | 0.006120 |
| NonParamDML | 0.005975 |

Both DML estimators showed lower mean absolute ATE bias than the Difference-in-Means baseline across these five evaluation runs.

NonParamDML had marginally lower mean absolute ATE bias. LinearDML performed better on individual treatment-effect prediction metrics, including MAE, RMSE, and effect correlation.

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

## 12. Automated Tests

Automated tests are included in:

`tests/test_dynamic_pricing.py`

The tests cover the dynamic-pricing functionality and related calculations.

The last recorded test result was:

**26 tests passed.**

This is the previously recorded result and should be confirmed by running the full test suite again before final submission.

Run:

```bash
pytest
```

## 13. Limitations and Critical Analysis

### 13.1 Synthetic Data Limitations

The dynamic-pricing experiment uses synthetic customer data and a controlled purchase-probability formula.

Although this allows comparison against known simulation assumptions, it cannot fully represent real customer behaviour, market competition, inventory constraints, or operational costs.

### 13.2 Observational Retail Data

The Online Retail dataset is observational.

Price and quantity may be affected by product characteristics, promotions, seasonality, customer composition, and other confounding factors.

Therefore, the observed price-quantity relationships cannot automatically be interpreted as causal price effects.

### 13.3 Holdout ATE Bias and Repeated-Seed Sensitivity

The initial holdout evaluation showed that the estimated ATE was higher than the synthetic reference ATE:

- True ATE: 0.074861.
- Estimated ATE: 0.092794.
- ATE bias: +0.017932 (approximately +1.79 percentage points).

To investigate whether this result was specific to one train/test partition, both DML estimators were evaluated across five random seeds: 42, 7, 21, 35, and 99.

The repeated-seed evaluation produced the following mean absolute ATE bias:

| Estimator | Mean Absolute ATE Bias |
|---|---:|
| Difference-in-Means baseline | 0.016959 |
| LinearDML | 0.006120 |
| NonParamDML | 0.005975 |

Both DML estimators showed lower mean absolute ATE bias than the Difference-in-Means baseline across these five runs. NonParamDML had a marginally lower mean absolute ATE bias, while LinearDML performed better on individual treatment-effect prediction metrics, including MAE, RMSE, and effect correlation.

**Seed 42 investigation:** The five-seed evaluation identified seed 42 as a particularly sensitive partition. Its raw treatment-group purchase-rate difference was approximately 9.07% in the training set but 3.72% in the holdout set. Both DML estimators overestimated the synthetic reference ATE on this split: LinearDML by approximately 1.79 percentage points and NonParamDML by approximately 1.60 percentage points. The other four seeds showed substantially smaller absolute ATE biases.

This result suggests sensitivity to the train/test partition and possible variation in the observed treatment-group outcomes. It does not establish overfitting or identify a definitive cause.

**Mitigation and further work:**

The current evaluation has already compared both DML estimators with the Difference-in-Means baseline across five random seeds and reported ATE bias alongside individual-effect prediction metrics.

Further work should include:

- Running additional seeds to strengthen the robustness assessment.
- Testing alternative train/test partitions.
- Investigating treatment-outcome variation across partitions.
- Reporting uncertainty intervals where statistically appropriate.
- Evaluating the estimators under alternative synthetic data-generating scenarios.

**Limitation:** These findings are based on five evaluation seeds and a synthetic pricing dataset. They provide useful diagnostic evidence but are not sufficient to establish general estimator superiority or real-world pricing effectiveness.

### 13.4 Pricing-Policy Limitations

The 5% discount produced the highest expected profit among the five tested policies, but the improvement over no discount was only approximately 0.53%.

The comparison depends on the synthetic purchase-probability model and illustrative product-cost assumptions.

Additional validation is required before making any real-world pricing recommendation.

### 13.5 Generalisation and Reproducibility

The results are dependent on the selected datasets, modelling assumptions, and evaluation partitions.

The five-seed evaluation provides more evidence than a single holdout split, but additional seeds and alternative data-generating scenarios are needed to assess robustness more thoroughly.

The reported results should be reproduced from the repository before final submission.

## 14. Scientific Conclusion

The EconoCausal project demonstrates how causal inference, machine learning, and statistical analysis can support customer-level decision-making and pricing-policy evaluation.

The Hillstrom randomized marketing experiment provides evidence about the effects of email campaigns on customer visits and conversions. The Online Retail dataset provides an opportunity to explore historical product sales, price variations, and demand patterns. The synthetic pricing experiment allows treatment-effect estimators and pricing policies to be evaluated against known simulation assumptions. These three components address different analytical questions and should be interpreted separately.

In the synthetic pricing experiment, both LinearDML and NonParamDML showed lower mean absolute ATE bias than the Difference-in-Means baseline across five evaluation seeds. LinearDML performed better on individual treatment-effect prediction metrics, including MAE, RMSE, and effect correlation, while NonParamDML showed marginally lower mean absolute ATE bias. These results indicate that estimator performance depends on the evaluation objective.

The repeated-seed analysis also revealed sensitivity to the train/test partition, particularly for seed 42. Therefore, results from a single holdout split should not be treated as conclusive evidence of model performance. Additional evaluation across more seeds and alternative data partitions is required to assess robustness.

The synthetic dynamic-pricing comparison identified the 5% discount as the highest-profit option among the five tested policies. However, its advantage over the no-discount policy was approximately 0.53%. Since the experiment uses synthetic customer data and illustrative product-cost assumptions, this finding does not establish that a 5% discount is optimal for a real business.

The Online Retail analysis did not identify a statistically significant price-quantity relationship among the five selected products or in the pooled regression. Because the data are observational and the analysis has limited product-level monthly observations, these findings should be interpreted as exploratory rather than causal evidence about price elasticity.

Overall, the project provides a foundation for studying randomized marketing effects, observational product-demand patterns, synthetic causal estimation, and pricing-policy evaluation. Further work should focus on multi-treatment causal estimation, additional robustness checks, sensitivity analysis, realistic cost assumptions, and appropriate real-world validation.

The project demonstrates the importance of evaluating not only model predictions but also estimation error, experimental assumptions, reproducibility, and business relevance. Its current results are useful for research and educational purposes but should not be treated as validated real-world pricing recommendations.

## 15. Future Improvements and Development Roadmap

### Phase 1 — Current Project Foundation

- Complete the initial data analysis.
- Implement the synthetic pricing experiment.
- Implement and compare DML estimators.
- Evaluate candidate discount policies.
- Add automated tests and project documentation.

### Phase 2 — Robustness and Validation

- Extend the existing five-seed evaluation using additional random seeds and alternative data partitions.
- Investigate treatment-effect estimation stability.
- Add uncertainty intervals where statistically appropriate.
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

**Project status:** The project has a working analytical foundation, recorded validation results, pricing-policy comparisons, and automated tests. Final reproducibility checks, integration review, and submission-quality verification remain necessary before claiming full project completion.
