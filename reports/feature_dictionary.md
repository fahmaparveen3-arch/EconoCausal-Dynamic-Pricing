# Feature Dictionary

## 1. Purpose

This document describes the key variables used in the EconoCausal: Dynamic Pricing via Double Machine Learning project. It helps make the dataset easier to understand and supports reproducible data analysis.

## 2. Dataset Overview

The project uses a synthetic dataset containing simulated customer records and discount levels. The dataset is intended to explore relationships between discounts, customer purchasing behaviour, and profitability.

## 3. Key Variable Categories

| Variable category | Meaning | Purpose |
|---|---|---|
| Customer identifier | Unique identifier for a customer or record, if available | Identifies records and helps detect duplicates |
| Discount level | Discount assigned to a customer | Represents the treatment variable |
| Purchase outcome | Indicates whether a purchase occurred | Represents the outcome variable for conversion analysis |
| Revenue | Revenue associated with a customer or transaction, if available | Supports revenue analysis |
| Product cost | Cost associated with a product or sale, if available | Supports profit calculations |
| Customer characteristics | Available customer attributes | May be used as covariates in causal analysis |
| Estimated treatment effect | Model-estimated effect of a discount, if generated | Helps investigate variation in customer responses |

## 4. Treatment and Outcome

The discount assignment is the treatment variable. The purchase outcome is a key outcome for estimating the effect of discounts on customer purchasing behaviour.

The exact column names and definitions must be confirmed against the dataset and the model code before analysis.

## 5. Data-Type Checks

- Identifiers should be handled consistently.
- Discount values should use a suitable numeric representation.
- Binary purchase outcomes should use consistent values.
- Revenue, costs, and profit should use appropriate numeric data types.
- Categorical features should have consistent labels.

## 6. Important Considerations

An estimated treatment effect is a model output, not necessarily an original dataset column. Similarly, profit may be calculated from revenue and cost rather than supplied directly.

Only variables that actually exist in the project should be included in the final dataset schema.

## 7. Conclusion

A clear feature dictionary improves collaboration, helps prevent incorrect variable usage, and makes the project's data-preparation and causal-analysis workflow easier to understand.