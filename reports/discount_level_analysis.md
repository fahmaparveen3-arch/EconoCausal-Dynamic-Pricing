# Discount Level Analysis

## 1. Objective

The objective of this analysis is to compare discount policies based on expected customer purchase rates and profitability in the EconoCausal Dynamic Pricing project.

## 2. Dataset Overview

The project uses a synthetic dataset containing 10,000 simulated customer records. Five discount policies were evaluated:

- 0% discount
- 5% discount
- 10% discount
- 15% discount
- 20% discount

The policy comparison was generated using the same set of 10,000 simulated customers.

**Important:** The dataset is synthetic. These results are illustrative and do not establish how real customers would respond to discounts.

## 3. Pricing Policy Comparison

The latest reported policy comparison produced the following results:

| Discount | Expected Purchase Rate | Expected Profit per Customer | Total Expected Profit |
|---:|---:|---:|---:|
| 0% | 20.78% | 33.24 | 332,435.25 |
| 5% | 23.54% | 33.42 | 334,186.01 |
| 10% | 26.53% | 32.85 | 328,546.76 |
| 15% | 29.72% | 31.41 | 314,052.64 |
| 20% | 33.11% | 28.93 | 289,266.88 |

These figures are based on the project's latest reported policy-comparison results and should be checked against `reports/pricing_policy_comparison.csv` before final submission.

## 4. Key Findings

### Purchase Rate

The expected purchase rate increases as the discount rises, from 20.78% with no discount to 33.11% with a 20% discount.

This suggests that, within the synthetic evaluation, larger discounts are associated with higher expected purchase rates.

### Profitability

The 5% discount policy produced the highest reported expected profit per customer, at 33.42, and the highest total expected profit, at 334,186.01.

Compared with the no-discount policy, the 5% policy increased total expected profit by approximately 0.53%.

The 20% discount policy achieved the highest expected purchase rate but the lowest total expected profit among the five policies.

## 5. Interpretation

Purchase rate and profitability are different measures of performance. Although larger discounts may encourage more purchases, they can also reduce the profit earned per sale.

In this evaluation, a 5% discount provided a better expected profit outcome than the other tested policies. Therefore, choosing a pricing policy based only on purchase rate could lead to a less profitable decision.

The 5% discount should be considered the best-performing policy among the five tested options under the current simulation assumptions, not a proven real-world optimum.

## 6. Validation and Further Work

The following tasks should be completed before final submission:

1. Verify the results against `reports/pricing_policy_comparison.csv`.
2. Review the purchase-probability and expected-profit formulas.
3. Check the assumptions used for product costs and discount costs.
4. Evaluate model performance and the reliability of causal-effect estimates.
5. Perform sensitivity analysis using different cost and customer-response assumptions.
6. Keep the synthetic pricing-policy results separate from the Hillstrom email-marketing experiment.

## 7. Limitations

- The pricing dataset contains simulated rather than real customer behaviour.
- Results depend on the assumptions used to generate the data and calculate expected profit.
- Operating expenses may not be included in the reported profit calculations.
- Only five discount levels were compared.
- The analysis does not establish that the same pricing policy would be optimal in a real business.

## 8. Conclusion

The latest policy comparison shows a trade-off between customer purchase rate and expected profitability. The 20% discount produced the highest expected purchase rate, while the 5% discount produced the highest expected profit among the five tested policies.

These findings demonstrate the importance of evaluating pricing strategies using profit-based metrics alongside customer-response measures. Further validation and sensitivity analysis are required before making real-world pricing recommendations.

## Pricing Results Validation

The discount-policy results in this report were cross-checked against `reports/pricing_policy_comparison.csv` from the Hiba branch.

### Validation Findings
- The comparison evaluates five discount levels: 0%, 5%, 10%, 15%, and 20%.
- The 5% discount achieves the highest expected total profit of 334,186.01.
- The 20% discount achieves the highest expected purchase rate of 33.11%.
- Expected total profit is lower at discount levels above 5% in the tested scenarios.

### Limitations
The results are based on 10,000 simulated customers. They depend on the model and pricing assumptions used in the experiment and should not be interpreted as proof of real-world profitability. Further validation using real transaction data and sensitivity analysis is recommended.