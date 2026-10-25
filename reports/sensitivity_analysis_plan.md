# Sensitivity Analysis Plan

## 1. Objective

The objective of sensitivity analysis is to investigate whether the project's pricing conclusions remain consistent when key assumptions change.

The analysis focuses on the relationship between discount levels, customer purchasing behaviour, product costs, and estimated profit.

## 2. Key Factors

The following factors may affect the results:

- Product cost assumptions.
- Discount levels.
- Customer purchase rates.
- Revenue per customer.
- Assumptions used to generate the synthetic dataset.

## 3. Proposed Analysis

### Product Cost Sensitivity
Evaluate how changes in assumed product costs affect profit at each discount level.

### Discount-Level Comparison
Compare the estimated profit associated with discounts of 0%, 5%, 10%, 15%, and 20%.

### Purchase Behaviour
Investigate how changes in purchase rates affect revenue and profitability.

### Best Discount Stability
Check whether the discount with the highest estimated profit remains the same under different reasonable assumptions.

## 4. Evaluation Metrics

Where supported by the existing project code, compare:

- Purchase rate.
- Average revenue per customer.
- Average profit per customer.
- Total profit.
- Discount level with the highest estimated profit.

## 5. Interpretation

If the same discount remains most profitable under different reasonable assumptions, the decision may be more robust within the tested scenarios.

If the preferred discount changes substantially, the decision is sensitive to those assumptions and requires further investigation.

## 6. Limitations

This analysis depends on the quality of the synthetic dataset and the assumptions used to calculate profit. Changing assumptions does not establish how real customers would respond to discounts.

The scenarios and their results must be documented transparently. No sensitivity-analysis results should be reported until the analysis has actually been performed.

## 7. Conclusion

Sensitivity analysis can help determine whether a pricing recommendation depends heavily on specific assumptions. It provides an additional check before using the project's results to inform pricing decisions.