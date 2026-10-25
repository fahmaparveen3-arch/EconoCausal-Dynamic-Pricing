# Double Machine Learning Methodology

## 1. Objective

The objective of EconoCausal is to investigate how discounts influence customer purchasing behaviour and business profit. The project uses causal inference techniques to estimate the effect of pricing interventions while accounting for relevant customer characteristics.

## 2. Why Double Machine Learning?

A simple comparison between customers who receive discounts and those who do not may be misleading because the two groups can have different characteristics.

Double Machine Learning (DML) helps estimate treatment effects while controlling for observed confounding variables using machine learning models.

## 3. Key Variables

- **Treatment (T):** The discount or pricing intervention applied to a customer.
- **Outcome (Y):** The selected business outcome, such as purchase behaviour or profit.
- **Covariates (X):** Observed customer or transaction characteristics that may influence treatment assignment and the outcome.

The exact variables will depend on the available pricing dataset.

## 4. Proposed Workflow

1. Load and inspect the pricing dataset.
2. Clean the data and validate variable types.
3. Identify the treatment, outcome, and covariates.
4. Explore relationships between variables.
5. Train the nuisance models used by the DML estimator.
6. Estimate treatment effects using an appropriate DML estimator.
7. Evaluate the estimates and compare candidate pricing policies.
8. Document assumptions, limitations, and findings.

## 5. Model Evaluation

The analysis should examine:

- Data quality and missing values.
- Treatment and outcome distributions.
- Stability of estimated treatment effects.
- Sensitivity to modelling choices.
- Expected profit under alternative discount policies.
- Whether conclusions change under reasonable alternative assumptions.

## 6. Assumptions and Limitations

Causal estimates depend on assumptions about confounding, treatment assignment, and data quality. Observational data may contain unmeasured confounders, which can bias estimates.

Results obtained from synthetic data demonstrate the workflow but do not establish that a pricing policy will improve real-world profit.

## 7. Next Steps

- Confirm the treatment, outcome, and covariates in the pricing dataset.
- Implement the DML estimator.
- Evaluate model behaviour and treatment-effect estimates.
- Compare pricing policies using clearly documented assumptions.
- Record limitations before presenting recommendations.
