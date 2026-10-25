# EconoCausal — Dynamic Pricing

## Project Overview

EconoCausal explores causal inference, uplift modelling, and data-driven pricing strategies. The project investigates how treatment effects can support customer-level decisions in a simulated discount-pricing environment.

## Project Structure

- `data/` — Datasets and prepared pricing data.
- `notebooks/` — Exploratory data analysis and experiments.
- `src/data_processing/` — Data loading, validation, and dataset preparation.
- `src/models/` — Machine-learning and Double Machine Learning models.
- `src/evaluation/` — Model evaluation, pricing profit evaluation, and policy comparison.
- `src/pricing/` — Pricing calculations and pricing logic.
- `reports/` — Generated analysis results and customer-level estimates.
- `figures/` — Saved charts.
- `docs/` — Project documentation.
- `tests/` — Automated tests for pricing functionality.

## Current Progress

- Explored the Hillstrom email campaign experiment.
- Compared email treatment groups with the no-email control group.
- Created a synthetic discount-pricing dataset containing 10,000 customer records.
- Added scripts to load, validate, and prepare the synthetic pricing data.
- Implemented a Double Machine Learning (DML) model using EconML.
- Generated customer-level estimated treatment effects and saved them to `reports/dml_customer_effects.csv`.
- Implemented a pricing profit evaluation script to compare revenue and simulated profit across discount levels.
- Saved pricing evaluation results to `reports/pricing_profit_evaluation.csv`.
- Implemented a pricing policy comparison that evaluates five discount levels on the same customer records.
- Saved policy comparison results to `reports/pricing_policy_comparison.csv`.
- Added automated tests for the dynamic-pricing functionality.
- Added EconML to `requirements.txt`.

## Running the Synthetic Pricing DML Model

Run these commands from the project root in a terminal.

### 1. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 2. Generate the synthetic pricing dataset

```bash
python src/data_processing/generate_synthetic_pricing_data.py
```

### 3. Prepare the dataset

```bash
python src/data_processing/prepare_pricing_data.py
```

### 4. Train the DML model

```bash
python src/models/train_dml.py
```

The model reads `data/prepared_pricing.csv` and saves estimated customer-level treatment effects to `reports/dml_customer_effects.csv`.

## Running the Pricing Profit Evaluation

The profit evaluation script compares revenue and estimated profit across discount levels using the synthetic pricing dataset.

### 1. Run the evaluation

```bash
python src/evaluation/evaluate_pricing_profit.py
```

### 2. View the results

The script saves the results to `reports/pricing_profit_evaluation.csv`.

The report includes:

- Number of customers in each discount group.
- Purchase rate for each discount group.
- Total revenue and mean revenue per customer.
- Estimated product costs.
- Total simulated profit.
- Mean simulated profit per customer.

### 3. Interpret the results

In the current synthetic dataset:

- The **0% discount group** has the highest mean simulated profit per customer, approximately **36.32**.
- Among the discounted groups, the **15% discount group** has the highest mean simulated profit per customer, approximately **32.01**.
- The **20% discount group** has the highest purchase rate and mean revenue per customer among the five discount groups.

These results illustrate that a higher purchase rate or revenue does not necessarily mean higher profit.

**Important:** These are descriptive results from groups with different customer counts and characteristics. They should not be interpreted as a fair comparison of all discount policies. Product-cost ratios are illustrative assumptions, and simulated profit excludes operating expenses, marketing costs, taxes, shipping, and other business expenses.

## Running the Pricing Policy Comparison

This evaluation compares five discount policies — 0%, 5%, 10%, 15%, and 20% — using the same 10,000 synthetic customers. Each candidate discount is evaluated using the same customer characteristics and the synthetic purchase-probability formula.

### 1. Run the comparison

```bash
python src/evaluation/compare_pricing_policies.py
```

### 2. View the results

The script saves the results to `reports/pricing_policy_comparison.csv`.

The report includes:

- Discount rate.
- Number of customers evaluated.
- Expected purchase rate.
- Expected revenue per customer.
- Expected profit per customer.
- Total expected revenue.
- Total expected profit.

### 3. Results

Under the current simulation assumptions, the **5% discount policy** produces the highest expected profit per customer.

| Discount | Expected purchase rate | Expected profit per customer | Total expected profit |
|---:|---:|---:|---:|
| 0% | 20.78% | 33.24 | 332,435.25 |
| 5% | 23.54% | 33.42 | 334,186.01 |
| 10% | 26.53% | 32.85 | 328,546.76 |
| 15% | 29.72% | 31.41 | 314,052.64 |
| 20% | 33.11% | 28.93 | 289,266.88 |

The 5% policy produces an estimated total expected profit of **334,186.01**, compared with **332,435.25** for the 0% policy. This is an estimated improvement of approximately **0.53%**.

The results show that increasing the discount raises the expected purchase rate, but larger discounts can reduce profit because the price reduction outweighs the benefit of additional purchases.

### 4. Assumptions and interpretation

- All five policies are evaluated using the same customer records.
- The purchase-probability formula follows the assumptions used in the synthetic data generator.
- Expected units per purchase are assumed to be 1.15, based on the synthetic data generator's unit distribution.
- Product-cost ratios are illustrative assumptions.
- Profit excludes operating and other business expenses.
- The comparison is a model-based simulation, not a real-world experiment.
- The 5% policy performs best under the current assumptions, but the small estimated advantage over 0% should be interpreted cautiously.

## Automated Tests

The project includes automated tests for the dynamic-pricing functionality.

Run the tests from the project root:

```bash
python -m pytest -v
```

The current test suite contains 11 tests covering discounted-price calculations, input validation, purchase-probability estimation, expected-profit calculations, and comparison of candidate discounts.

**Latest verification:** All 11 tests passed.

## Important Limitations

- The Hillstrom dataset evaluates email campaign effectiveness. It does not directly measure the effect of discounts or establish an optimal pricing strategy.
- The synthetic pricing dataset is simulated. Results from it do not establish real-world business impact.
- The current DML model estimates the effect of receiving a discount treatment versus control. It does not yet estimate the causal effect of each individual discount percentage or independently establish the profit-maximizing pricing strategy.
- The pricing profit evaluation is descriptive and compares observed synthetic outcomes across groups that may differ in customer composition and group size.
- The policy comparison evaluates hypothetical discount policies using a specified purchase-probability model and illustrative product-cost ratios.
- The policy comparison's expected profit estimates depend on the model assumptions, including the expected number of units sold per purchase.
- Product-cost ratios are assumptions rather than actual business costs.
- Profit estimates exclude operating expenses and other business costs.
- The 5% discount result is not proof that 5% is optimal in a real business.
- Model results are exploratory and require further validation before practical business recommendations are made.

## Team Note

The project is under development. Data preparation, causal modelling, evaluation, testing, and pricing optimization should be reviewed and validated before the results are used for business decisions.
