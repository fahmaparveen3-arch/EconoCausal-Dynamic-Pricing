# EconoCausal — Dynamic Pricing

## Project Overview
EconoCausal explores causal inference, uplift modelling, and data-driven pricing strategies.

## Project Structure
- `data/` — Local datasets (subject to usage and licensing terms).
- `notebooks/` — Exploratory data analysis and experiments.
- `src/data_processing/` — Data loading and validation.
- `src/models/` — Machine-learning models.
- `src/evaluation/` — Model evaluation utilities.
- `src/pricing/` — Pricing calculations and future pricing logic.
- `reports/` — Analysis reports.
- `figures/` — Saved charts.
- `docs/` — Project documentation.

## Current Progress
- Explored the Hillstrom email campaign experiment.
- Compared email treatment groups with the no-email control group.
- Built preliminary conversion and uplift modelling experiments.
- Created starter modules for data processing, modelling, evaluation, and discount calculations.

## Important Limitation
The Hillstrom dataset evaluates email campaign effectiveness. It does not directly measure the effect of discounts or establish an optimal pricing strategy. A separate, suitable pricing dataset and a validated pricing methodology are needed for the dynamic-pricing component.

## Team Note
Model results are exploratory and require further validation before practical business recommendations are made.
