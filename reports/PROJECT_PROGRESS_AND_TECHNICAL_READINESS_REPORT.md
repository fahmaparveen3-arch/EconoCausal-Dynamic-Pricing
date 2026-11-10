# EconoCausal â€“ Dynamic Pricing
## Project Progress and Technical Readiness Report

**Date:** 10 November 2026
**Project:** Infotact Project 2
**Repository:** fahmaparveen3-arch/EconoCausal-Dynamic-Pricing

### 1. Project Overview

EconoCausal is an analytical platform combining causal inference, uplift modelling, Double Machine Learning (DML) and dynamic pricing analysis.

The project aims to evaluate customer responses to marketing treatments and pricing strategies and present analytical findings through an interactive dashboard.

### 2. Completed Work

**Data preparation**
- Explored the Hillstrom randomized email marketing dataset.
- Worked with 64,000 customer records and 12 original columns.
- Prepared a separate synthetic pricing dataset containing 10,000 customer records.
- Performed data quality and validation checks.

**Causal analysis**
- Estimated the effect of men's email treatment at +0.681 percentage points.
- Estimated the effect of women's email treatment at +0.311 percentage points.
- Both effects were statistically significant in the earlier analysis.

**Uplift modelling**
- Developed a T-learner uplift modelling workflow.
- Recorded a Qini coefficient of 0.8665.
- Recorded predicted mean uplift of approximately +0.632 percentage points.
- Evaluated observed test ATE and top-customer uplift.

**Dynamic pricing**
- Compared five discount strategies: 0%, 5%, 10%, 15% and 20%.
- Recorded the highest expected profit per customer at the 5% discount.
- Used synthetic pricing data to evaluate the pricing strategies.

**DML experiments**
- Implemented Double Machine Learning experiments.
- Compared model configurations and estimators.
- Performed holdout and repeated-seed validation.
- Recorded bias, MAE, RMSE and treatment-effect evaluation metrics.

### 3. Dashboard and Backend Development

The dashboard contains the following sections:

1. Overview
2. Pricing Analytics
3. Causal Analysis
4. Uplift Analysis
5. Model Insights

Backend functionality includes:
- FastAPI-based endpoints.
- Dynamic data loading.
- Dataset validation.
- API error handling.
- Report export functionality.
- Frontend integration and dynamic dashboard updates.

The dashboard integration milestone was committed and pushed to the Hiba branch in commit `6708316`.

The separate Fahma branch contains the Overview Metrics API implementation and tests in commit `c8e6dfd`.

### 4. Testing and Validation Status

Previously reported verification includes:
- Backend API endpoint checks.
- Python syntax validation.
- Frontend production build.
- Dashboard manual testing.
- API response and error-handling checks.
- Automated backend tests.

The Fahma branch's Day 21 API work passed 28 tests, including the new Overview API tests.

A Starlette TestClient deprecation warning was observed during testing. It did not prevent the tests from passing.

### 5. Current Technical Readiness

The dashboard and backend integration milestone is complete according to the latest project progress report.

However, the full project still requires a final verification process before submission.

The following areas need additional review:

- Original Infotact Project 2 requirements.
- Notebook execution and reproducibility.
- Dataset sources and data documentation.
- DML validation results and metric definitions.
- Model assumptions and limitations.
- Dependency installation and setup instructions.
- Complete frontend and backend integration.
- Final GitHub repository review.

### 6. Pending Work

| Task | Status |
|---|---|
| Original requirements audit | Pending |
| Notebook execution review | Pending |
| Dataset reproducibility | Pending |
| DML results verification | Pending |
| Model assumptions review | Pending |
| README and documentation review | Pending |
| Complete integration testing | Pending |
| Final submission checklist | Pending |

### 7. Scientific Limitations

The Hillstrom dataset supports randomized email treatment analysis.

The synthetic pricing dataset demonstrates a pricing-analysis workflow but does not establish real-world pricing effectiveness.

Uplift metrics and DML estimates must be interpreted according to their definitions, experimental design and validation results.

The project should not claim proven real-world profit improvements.

### 8. Next Development Phase

The next phase will focus on project verification rather than unnecessary feature development.

Planned activities:

1. Audit the original Infotact requirements.
2. Compare each requirement with the existing repository.
3. Review notebooks and reproduce important results.
4. Verify the DML and uplift modelling methodology.
5. Improve documentation where necessary.
6. Perform final integration and submission checks.

### 9. Conclusion

EconoCausal has progressed from individual analytical experiments to an integrated dashboard and backend application.

The project demonstrates practical experience with Python, machine learning, causal inference, uplift modelling, FastAPI, data validation and dashboard development.

The dashboard integration milestone is complete. Final reproducibility, documentation and requirements verification remain necessary before declaring the project submission-ready.
