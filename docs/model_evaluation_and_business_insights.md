# Model Evaluation and Business Insights

## 1. Introduction

This document summarizes the evaluation of the experimental uplift model,
Double Machine Learning (DML) analysis, and synthetic dynamic pricing
experiments conducted in the EconoCausal project.

The objective is to understand treatment effectiveness, evaluate model
performance, and identify potential business insights.

## 2. Hillstrom Experiment Analysis

The Hillstrom dataset contains approximately 64,000 customer records.

### Campaign Conversion Rates

| Campaign | Conversion Rate |
|---|---:|
| No Email | 0.573% |
| Men's Email | 1.253% |
| Women's Email | 0.884% |

### Estimated Treatment Effects

- Men's Email vs No Email: +0.681 percentage points.
- Women's Email vs No Email: +0.311 percentage points.

Both estimated effects were statistically significant.

### Business Insight

The Men's Email campaign showed a higher conversion rate than the
other campaign groups in this experiment.

This suggests that targeted marketing campaigns may improve customer
conversion compared with sending no campaign.

## 3. Uplift Model Evaluation

The uplift modelling analysis used a corrected T-learner approach.

### Evaluation Results

| Metric | Result |
|---|---:|
| Predicted uplift | 0.632 percentage points |
| Observed test-set treatment effect | 0.832 percentage points |
| Qini coefficient | 0.8665 |
| Top 20% predicted uplift | +1.313 percentage points |

### Business Insight

The uplift model helps identify customers who may respond more
positively to a marketing intervention.

Businesses can use customer-level uplift predictions to prioritize
marketing campaigns and improve targeting efficiency.

These results should be interpreted within the limitations of the
experimental dataset.

## 4. Double Machine Learning Evaluation

Double Machine Learning was evaluated using synthetic data.

### Full Dataset Results

| Metric | Result |
|---|---:|
| True ATE | 0.074463 |
| Estimated ATE | 0.079521 |
| MAE | 0.016636 |
| RMSE | 0.020166 |

### Holdout Dataset Results

| Metric | Result |
|---|---:|
| True ATE | 0.074861 |
| Estimated ATE | 0.092794 |
| MAE | 0.020994 |
| RMSE | 0.024203 |

### Interpretation

The estimated treatment effects were reasonably close to the
known synthetic treatment effects.

The holdout results show some estimation error, highlighting the
importance of evaluating causal models on unseen data.

## 5. Synthetic Dynamic Pricing Analysis

A synthetic pricing dataset containing 10,000 records was used to
evaluate different discount strategies.

### Expected Profit per Customer

| Discount Rate | Expected Profit |
|---|---:|
| 0% | $33.24 |
| 5% | $33.42 |
| 10% | $32.85 |
| 15% | $31.41 |
| 20% | $28.93 |

### Business Insight

The 5% discount strategy produced the highest expected profit per
customer among the tested discount levels.

Higher discount rates showed lower expected profit in this
synthetic experiment.

The 5% result is specific to the assumptions and data used in
the simulation. It should not be treated as a proven optimal
discount for real-world customers.

## 6. Online Retail Observational Analysis

An observational analysis was conducted using the Online Retail data.

The estimated price coefficient was 0.3691, with a p-value of
0.7658.

The result was not statistically significant.

### Interpretation

The analysis did not provide sufficient statistical evidence of
a significant price effect in this observational dataset.

Because the data is observational, the estimated relationship
should not be interpreted as a causal effect.

## 7. Overall Business Recommendations

1. Use experimental evidence to evaluate marketing campaign effectiveness.
2. Consider uplift modelling for customer targeting.
3. Evaluate pricing strategies using expected profit rather than
   conversion rate alone.
4. Validate synthetic pricing recommendations using real-world data.
5. Evaluate causal models on holdout datasets.
6. Avoid making causal claims from observational results without
   appropriate identification assumptions.

## 8. Limitations

- Synthetic pricing results depend on simulation assumptions.
- Hillstrom campaign results come from a specific experimental dataset.
- Uplift predictions may not generalize to every customer population.
- Online Retail observational analysis does not establish causality.
- Model performance should be monitored when applied to new data.

## 9. Conclusion

The EconoCausal project combines experimental analysis, uplift
modelling, Double Machine Learning, and dynamic pricing simulation.

The results demonstrate how causal analysis can support marketing
and pricing decisions while highlighting the importance of model
validation, statistical significance, and responsible interpretation.