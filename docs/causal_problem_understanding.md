# EconoCausal: Dynamic Pricing via Double Machine Learning

## 1. Project Objective

To estimate the causal effect of discounts on customer purchasing behaviour using Double Machine Learning (DML) and support data-driven pricing decisions.

## 2. Problem Statement

Traditional machine learning models can predict whether a customer is likely to purchase a product, but they do not necessarily identify whether a discount causes that customer to purchase.

EconoCausal aims to estimate the effect of different discount amounts on purchasing behaviour while accounting for other relevant factors.

## 3. Key Variables

### Treatment Variable
- Discount amount offered to the customer.

### Outcome Variable
- Purchase status: whether the customer purchased the product.

### Potential Confounding Variables
- Previous purchase history.
- Customer segment.
- Product category.
- Seasonality.
- Marketing campaign characteristics.

These variables are initial assumptions and must be checked against the selected dataset.

## 4. Initial Causal Assumptions

The discount offered may affect the probability of purchase. Customer characteristics, previous purchase behaviour, and campaign conditions may influence both discount assignment and purchasing behaviour.

The causal graph will be refined after reviewing the dataset and discussing the assumptions with the team.

## 5. Proposed Methodology

1. Select and understand a suitable retail or marketing dataset.
2. Perform data cleaning and exploratory data analysis.
3. Define the treatment, outcome, and confounders.
4. Construct a causal Directed Acyclic Graph (DAG) using DoWhy.
5. Estimate causal effects using Double Machine Learning with EconML.
6. Validate the estimates using appropriate causal refutation tests.
7. Explore discount allocation under a fixed budget using SciPy.

## 6. Week 1 Plan

- Research causal inference and Double Machine Learning.
- Identify a suitable mock retail dataset.
- Define the initial causal variables and DAG.
- Begin the causal analysis workflow using DoWhy.
- Coordinate dashboard requirements with the team.

## 7. Day 1 Progress

- Reviewed the assigned EconoCausal project requirements.
- Documented the initial problem statement and objectives.
- Identified potential treatment, outcome, and confounding variables.
- Prepared the initial causal analysis plan.