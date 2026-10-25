# DML Model Validation Plan

## 1. Objective

This document outlines validation checks for the Double Machine Learning (DML) model used in the EconoCausal Dynamic Pricing project.

The goal is to evaluate the reliability of estimated discount effects on customer purchasing behaviour.

## 2. Model Overview

Double Machine Learning is a causal inference approach that uses machine learning to account for observed customer characteristics when estimating treatment effects.

In this project, discount assignment represents the treatment, and customer purchase behaviour is a key outcome.

The dataset currently contains simulated customer records, so model results must be interpreted within the assumptions of the simulation.

## 3. Validation Checklist

### Data Validation
- Confirm that treatment and outcome variables are correctly identified.
- Check for missing values and invalid observations.
- Verify that the features used by the model are available and correctly formatted.

### Treatment Distribution
- Count observations at each discount level.
- Check whether the dataset contains sufficient observations for meaningful comparisons.
- Investigate substantial imbalances between treatment groups.

### Model Configuration
- Review the treatment, outcome, and covariate definitions.
- Confirm the model configuration matches the intended causal question.
- Document the estimation method and relevant parameters.

### Estimate Stability
- Compare estimated effects across appropriate validation runs.
- Check whether results change substantially under reasonable modelling choices.
- Investigate unexpected patterns, including estimates that are positive across all discount levels.

### Evaluation
- Compare model estimates with observed group differences, while recognising that these measure different quantities.
- Review uncertainty estimates and confidence intervals where available.
- Avoid interpreting an estimated effect as proof of causation without considering the model assumptions.

## 4. Important Assumptions

The analysis should consider:

- Whether relevant confounders have been measured.
- Whether the covariates provide adequate adjustment for treatment assignment.
- Whether treatment groups have sufficient overlap in their observed characteristics.
- Whether the model specification is appropriate for the treatment and outcome.

A synthetic dataset may have known data-generating assumptions, but those assumptions must be inspected rather than presumed.

## 5. Reporting Results

A validation report should record:

1. The model and dataset version used.
2. The treatment and outcome definitions.
3. The estimated effects and their uncertainty.
4. The validation checks performed and their results.
5. Limitations and any unresolved issues.

## 6. Conclusion

Model validation is necessary before using DML estimates to support pricing decisions. The model's results should be evaluated alongside uncertainty, assumptions, and profit-based metrics.

Because the current dataset is synthetic, the findings should not be presented as proof of real-world customer behaviour.