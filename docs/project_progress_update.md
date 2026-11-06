# EconoCausal – Project Progress Update
**Date:** 6 November 2026

## 1. Project Overview
EconoCausal focuses on estimating the causal impact of marketing campaigns and pricing interventions using causal machine learning, including Double Machine Learning (DML).

## 2. Backend Progress
The backend work completed at the current project scope includes:
- Data collection, loading, cleaning, and exploratory data analysis.
- Hillstrom email campaign treatment-effect and uplift analysis.
- LinearDML and T-learner modelling.
- Discount treatment-effect analysis and dynamic pricing policy comparison.
- Model evaluation, validation, and robustness analysis.
- Automated tests, technical documentation, and reports.

## 3. Datasets
Three datasets were used for different analytical purposes:

1. **Hillstrom Email Marketing Dataset:** 64,000 records covering Men's Email, Women's Email, and No Email groups. Used for marketing treatment-effect and uplift analysis.
2. **UCI Online Retail Dataset:** Observational transaction data used to explore price, sales, and revenue patterns. It does not provide randomized pricing experiments.
3. **Synthetic Pricing Dataset:** 10,000 records and 14 columns, used to test pricing methods under controlled assumptions.

## 4. Key Analytical Results

### Hillstrom Campaign Analysis
- No Email conversion rate: 0.573%.
- Men's Email conversion rate: 1.253%.
- Women's Email conversion rate: 0.884%.
- Men's Email treatment effect versus No Email: approximately +0.681 percentage points.
- Women's Email treatment effect versus No Email: approximately +0.311 percentage points.
- Top 20% observed uplift: Random Forest T-learner 1.311 percentage points; HistGradientBoosting T-learner 1.305 percentage points.

### Predictive Model Evaluation
- Baseline conversion model ROC-AUC: 0.5490.
- Baseline conversion model PR-AUC: 0.0103.

### Synthetic Dynamic Pricing Experiment
Expected profit per customer under the tested discount policies:
- 0% discount: 33.24
- 5% discount: 33.42
- 10% discount: 32.85
- 15% discount: 31.41
- 20% discount: 28.93

The 5% discount produced the highest expected profit among the tested synthetic policies. This result is limited to the assumptions of the synthetic experiment and is not a real-world pricing guarantee.

### LinearDML Evaluation
- Full-data true ATE: 0.074463; estimated ATE: 0.079521.
- Full-data MAE: 0.016636; RMSE: 0.020166.
- Holdout true ATE: 0.074861; estimated ATE: 0.092794.
- Holdout MAE: 0.020994; RMSE: 0.024203.

The holdout estimate showed greater deviation from the true ATE than the full-data estimate.

### Online Retail Analysis
The estimated price coefficient was 0.3691 with p-value 0.7658. This result was not statistically significant. Since the dataset is observational, it cannot independently establish a causal price effect.

## 5. Testing and Validation
The team reported that 38 tests passed across the broader project test suite, including preprocessing, pricing calculations, DML evaluation, and pipeline checks.

On the Afnan branch, the pricing data validation test suite has separately been run with 10 passing tests. These are different test scopes and should not be treated as the same result.

## 6. Current Limitations
- Synthetic pricing results depend on the assumptions used to generate the data.
- Hillstrom is a marketing experiment, not a randomized pricing experiment.
- Online Retail data is observational and has limitations for causal inference.
- The baseline conversion model has limited predictive performance.
- Synthetic DML results do not guarantee performance on real-world data.
- Live pricing deployment and frontend/API integration are not yet complete.

## 7. Frontend Development Roadmap
The next phase is to build and integrate the application interface.

Proposed technologies:
- Next.js / React for the frontend.
- Supabase for PostgreSQL database and authentication.
- Python API for backend integration.
- Render for API hosting.
- Vercel for frontend deployment.
- Recharts for dashboard visualizations.

Planned tasks:
1. Set up the frontend project.
2. Configure Supabase and database connectivity.
3. Develop and connect the Python API.
4. Build dashboard and customer analytics pages.
5. Develop the pricing interface.
6. Add authentication and user roles.
7. Integrate frontend and backend.
8. Test and deploy the application.

## 8. Overall Status
The backend is reported as complete within the current reviewed scope. Frontend development, API integration, and application deployment remain future work.

The project should therefore be considered a backend-completed project with application integration and deployment still pending.
