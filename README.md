# EconoCausal — Dynamic Pricing

## Project Overview

EconoCausal explores causal inference, uplift modelling, and data-driven pricing strategies. The project investigates how treatment effects can support customer-level decisions in a simulated discount-pricing environment.

## Project Structure

- `data/` — Datasets and prepared pricing data.
- `notebooks/` — Exploratory data analysis and experiments.
- `src/data_processing/` — Data loading, validation, and dataset preparation.
- `src/models/` — Machine-learning and Double Machine Learning models.
- `src/evaluation/` — Model evaluation utilities.
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

## Important Limitations

- The Hillstrom dataset evaluates email campaign effectiveness. It does not directly measure the effect of discounts or establish an optimal pricing strategy.
- The synthetic pricing dataset is simulated. Results from it do not establish real-world business impact.
- The current DML model estimates the effect of receiving a discount treatment versus control. It does not yet estimate the optimal discount percentage or identify the profit-maximizing pricing strategy.
- Model results are exploratory and require further validation before practical business recommendations are made.

## Team Note

The project is under development. Data preparation, causal modelling, evaluation, and pricing optimization should be reviewed and validated before the results are used for business decisions.
