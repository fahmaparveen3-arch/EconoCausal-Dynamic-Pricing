# Online Retail EDA: Limitations and Recommendations

## 1. Introduction

The Online Retail dataset was used to explore transaction-level sales patterns, product-level price and quantity relationships, and regression results.

The analysis provides useful exploratory insights. However, several limitations must be considered before drawing business conclusions.

## 2. Limitations of Price–Quantity Correlation

The analysis examined five products:

| Product | Correlation | P-value |
|---|---:|---:|
| Lunch Bag Red Retrospot | -0.3388 | 0.2575 |
| Regency Cake Stand 3 Tier | +0.1984 | 0.5158 |
| Party Bunting | -0.0916 | 0.7660 |
| Jumbo Bag Red Retrospot | +0.1192 | 0.6982 |
| White Hanging Heart T-Light Holder | +0.0815 | 0.7911 |

None of the five correlations was statistically significant at the 5% level.

**Limitation:** These results do not establish that price has no relationship with quantity sold. They indicate that the analysis did not find statistically significant evidence of a linear relationship for these selected products.

## 3. Limitations of Regression Analysis

The fixed-effects regression produced the following results:

- Observations: 65
- Price coefficient: +0.3691
- Standard error: 1.2321
- T-statistic: 0.2995
- P-value: 0.7658

The estimated price coefficient was positive but statistically insignificant.

**Limitation:** The dataset is observational. Therefore, the regression cannot establish a causal relationship between price and demand. Other factors may influence purchasing behaviour.

## 4. Limitations of Monthly Aggregation

The analysis uses monthly aggregated observations for product-level relationships and regression.

Aggregation can hide differences between individual transactions and short-term changes in customer behaviour.

The limited number of observations may also reduce the ability to detect statistically significant relationships.

## 5. Missing CustomerID Values

Some records in the processed product-sales dataset have missing CustomerID values.

These records can still contribute to product-level transaction summaries. However, missing customer identifiers limit customer-level analysis, such as customer purchase frequency and individual purchasing patterns.

## 6. Recommendations for Further Analysis

The following improvements are recommended:

1. Examine price and quantity relationships using transaction-level data where appropriate.
2. Explore additional products instead of relying only on five selected products.
3. Investigate the influence of seasonal patterns and monthly trends.
4. Include relevant explanatory variables in future regression models.
5. Evaluate the impact of missing CustomerID values on customer-level analysis.
6. Use randomized experiments or appropriate causal inference methods when estimating causal price effects.

## 7. Conclusion

The Online Retail EDA provides useful exploratory information about product sales and price–quantity relationships.

However, the five selected product correlations and the fixed-effects regression do not provide statistically significant evidence of a price–quantity relationship.

The findings should be interpreted as exploratory rather than causal. Further analysis with suitable data and methodology is necessary before making pricing decisions.

