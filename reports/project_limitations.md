# Project Limitations

## 1. Overview

EconoCausal explores dynamic pricing using Double Machine Learning (DML), with the goal of understanding how different discount levels may affect customer purchasing behaviour and profitability.

Several limitations should be considered when interpreting the current results.

## 2. Synthetic Dataset

The current pricing dataset contains simulated customer records rather than verified real-world transactions.

Consequently, the observed patterns depend on the assumptions and relationships used to generate the data. They should not be treated as proof of actual customer behaviour.

## 3. Model Assumptions

DML estimates depend on appropriate treatment and outcome definitions, relevant covariates, sufficient overlap between treatment groups, and other modelling assumptions.

If these assumptions are not adequately satisfied, the estimated effects may be unreliable.

## 4. Treatment-Effect Interpretation

Differences in observed purchase rates across discount groups do not necessarily equal causal effects.

Model estimates should be interpreted alongside uncertainty measures, validation checks, and the assumptions underlying the analysis.

## 5. Profit Assumptions

Profit calculations depend on the product costs and other assumptions used by the evaluation code.

If these assumptions do not reflect a realistic business setting, the preferred discount may change.

## 6. Generalisability

Results from synthetic data may not transfer to real customers, products, or markets. Real-world pricing decisions would require suitable real-world data and further evaluation.

## 7. Future Improvements

Potential improvements include:

- Evaluating the model using appropriate validation procedures.
- Investigating the stability of treatment-effect estimates.
- Testing sensitivity to product-cost assumptions.
- Comparing purchase rate, revenue, and profit.
- Exploring suitable real-world datasets with relevant pricing and outcome information.
- Improving documentation and reproducibility.

## 8. Conclusion

The current project provides a framework for exploring causal approaches to dynamic pricing. Its findings should be considered preliminary until the modelling assumptions, validation results, and limitations have been carefully evaluated.