# Exploratory Data Analysis (EDA) Plan

## 1. Objective

The objective of Exploratory Data Analysis (EDA) is to understand the structure, quality, and distribution of the synthetic pricing dataset before conducting causal inference and profit analysis.

## 2. Dataset Overview

The project uses simulated customer data to investigate how different discount levels relate to purchasing behaviour and profitability.

The dataset should be inspected to confirm its number of records, available variables, data types, and missing-value patterns.

## 3. Analysis Tasks

### Dataset Structure
- Check the number of rows and columns.
- Review column names and data types.
- Identify missing and duplicate records.

### Discount Distribution
- Count the records assigned to each discount level.
- Compare the number of customers across the available discount groups.
- Check whether the discount groups are represented as expected.

### Purchase Behaviour
- Calculate the purchase rate for each discount level.
- Compare purchase rates across groups.
- Use a bar chart to communicate the differences.

### Revenue and Profit
- Compare average revenue per customer across discount levels.
- Compare profit per customer using the project's documented cost assumptions.
- Identify whether the discount level with the highest purchase rate also has the highest profit.

### Customer Characteristics
- Explore available customer features.
- Check whether customer characteristics vary across discount groups.
- Identify potential covariates relevant to causal analysis.

## 4. Visualisation Plan

The following visualisations may help communicate the findings:

1. Bar chart of customer counts by discount level.
2. Bar chart of purchase rates by discount level.
3. Comparison of average revenue by discount level.
4. Comparison of average profit by discount level.
5. Distribution plots for selected numerical customer features.

Only create visualisations for variables that actually exist in the dataset.

## 5. Interpretation and Limitations

Descriptive differences between discount groups do not automatically establish causal effects. The Double Machine Learning model must be evaluated separately.

Because the current dataset is synthetic, findings reflect the assumptions used to generate the data and should not be treated as verified real-world evidence.

## 6. Conclusion

EDA provides an initial understanding of the data and helps identify potential quality issues, group differences, and patterns that require further investigation before causal modelling.