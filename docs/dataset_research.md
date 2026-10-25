# EconoCausal: Dataset Research

## 1. Objective

Identify suitable datasets for studying the causal effect of marketing treatments and discounts on customer purchasing behaviour.

## 2. Existing Dataset: Hillstrom Email Marketing Experiment

**Purpose:** Marketing treatment-effect analysis.

**Dataset size:** 64,000 rows and 12 columns, as recorded in the team's previous analysis.

**Potential use:**
- Explore customer characteristics and purchase outcomes.
- Compare email treatment groups with the control group.
- Practise causal inference and uplift modelling using experimental data.

**Limitation:** The treatment is an email marketing campaign, not a product price or discount amount. Therefore, this dataset alone cannot directly estimate the causal effect of different discount levels.

## 3. Synthetic Retail Pricing Dataset

**Purpose:** Demonstrate the EconoCausal discount-pricing workflow.

**Planned variables:**
- Customer identifier
- Product category
- Original product price
- Discount percentage
- Discounted price
- Customer characteristics
- Purchase outcome
- Product cost

**Potential use:**
- Explore relationships between discount levels and purchases.
- Estimate treatment effects using Double Machine Learning.
- Compare revenue and simulated profit across pricing policies.

**Limitation:** Synthetic data are generated from assumptions and do not provide real-world evidence. Causal conclusions depend on the data-generating process and model assumptions.

## 4. Dataset Selection Decision

Retain the Hillstrom dataset for email marketing treatment-effect analysis and use the existing synthetic pricing dataset for the discount-pricing component.

Before final modelling, verify the synthetic data generator, variable definitions, treatment assignment, outcome generation, and product-cost assumptions.

## 5. Next Steps

1. Inspect the existing dataset generator and data preparation scripts.
2. Verify the treatment, outcome, and confounding variables.
3. Check data quality and discount-level distributions.
4. Confirm that the DML model and pricing evaluation use consistent definitions.
5. Document findings and limitations before making pricing recommendations.

## 6. Research Status

This document records the current dataset strategy. The exact synthetic data-generation assumptions and data-quality results must be verified against the implementation before final conclusions are drawn.