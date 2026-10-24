# EconoCausal — Dynamic Pricing

## Project Overview

EconoCausal explores causal inference, uplift modelling, and data-driven pricing strategies. The project investigates how treatment effects can support customer-level decisions in a simulated discount-pricing environment.

## Project Structure

- `data/` — Datasets and prepared pricing data.
- `notebooks/` — Exploratory data analysis and experiments.
- `src/data_processing/` — Data loading, validation, and dataset preparation.
- `src/models/` — Machine-learning and Double Machine Learning models.
- `src/evaluation/` — Model and pricing profit evaluation utilities.
- `src/pricing/` — Pricing calculations and future pricing logic.
- `reports/` — Generated analysis results.
- `figures/` — Saved charts.
- `docs/` — Project documentation.

## Current Progress

- Explored the Hillstrom email campaign experiment.
- Compared email treatment groups with the no-email control group.
- Created a synthetic discount-pricing dataset containing 10,000 customer records.
- Added scripts to load, validate, and prepare the synthetic pricing data.
- Implemented a Double Machine Learning (DML) model using EconML.
- Generated customer-level estimated treatment effects and saved them to `reports/dml_customer_effects.csv`.
- Implemented a pricing profit evaluation script to compare revenue and simulated profit across discount levels.
- Saved pricing evaluation results to `reports/pricing_profit_evaluation.csv`.
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

**Important:** Product-cost ratios are illustrative assumptions, not actual business costs. Simulated profit excludes operating expenses, marketing costs, taxes, shipping, and other business expenses.

## Important Limitations

- The Hillstrom dataset evaluates email campaign effectiveness. It does not directly measure the effect of discounts or establish an optimal pricing strategy.
- The synthetic pricing dataset is simulated. Results from it do not establish real-world business impact.
- The current DML model estimates the effect of receiving a discount treatment versus control. It does not yet estimate the effect of each individual discount percentage or identify the profit-maximizing pricing strategy.
- The pricing profit evaluation uses assumed product-cost ratios rather than actual business costs.
- The profit evaluation is descriptive and does not establish that one discount level will perform best in a real business.
- Model results are exploratory and require further validation before practical business recommendations are made.

## Team Note

The project is under development. Data preparation, causal modelling, evaluation, and pricing optimization should be reviewed and validated before the results are used for business decisions.
