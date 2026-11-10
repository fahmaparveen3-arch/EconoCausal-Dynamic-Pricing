# Project Reproducibility and Validation Review

## 1. Project Overview

**Project Name:** EconoCausal – Dynamic Pricing via Double Machine Learning

**Project Domain:** Data Science, Machine Learning, Causal Inference, and Dynamic Pricing

### Objective

The objective of this project is to develop a data-driven dynamic pricing analysis platform that combines causal inference, uplift modelling, and machine learning to evaluate the effects of pricing decisions on customer purchasing behaviour.

The project explores experimental and synthetic datasets to study treatment effects, customer responses, pricing strategies, and potential business outcomes.

### Key Components

- **Dataset Analysis:** Data exploration, cleaning, preprocessing, and validation.
- **Causal Inference:** Estimation of treatment effects using causal inference techniques.
- **Uplift Modelling:** Identification of customer groups with different responses to interventions.
- **Double Machine Learning (DML):** Estimation of treatment effects using machine learning-based nuisance models.
- **Dynamic Pricing Analysis:** Evaluation of different discount levels and their relationship with purchasing behaviour and expected profit.
- **Backend Development:** FastAPI services for data validation and dashboard metrics.
- **Frontend Dashboard:** Interactive dashboard for presenting pricing and causal analysis results.

### Project Data

The project uses the Hillstrom email marketing dataset for randomized treatment analysis and a synthetic pricing dataset for demonstrating pricing-related experiments.

The synthetic pricing dataset contains 10,000 records and 14 columns. Its results are intended for analytical demonstration and should not be interpreted as proof of real-world pricing effectiveness.

## 2. Dataset Preparation and Validation

### 2.1 Synthetic Pricing Dataset

The project uses a synthetic pricing dataset to demonstrate the dynamic pricing and causal analysis workflow.

**Dataset characteristics:**
- Total records: 10,000
- Total columns: 14
- Random seed: 42
- Discount levels: 0%, 5%, 10%, 15%, and 20%

### 2.2 Data Validation

Automated validation checks were developed to assess the quality and consistency of the pricing dataset.

The validation workflow includes:

- Checking whether the dataset is empty.
- Identifying missing values.
- Detecting duplicate records.
- Verifying required columns.
- Checking numeric data types and invalid values.
- Validating treatment and purchase indicators.
- Checking discount values against permitted ranges.
- Identifying non-finite numeric values.

### 2.3 Validation Results

The previously recorded validation results for the synthetic pricing dataset reported:

| Validation Check | Recorded Result |
|---|---:|
| Total records | 10,000 |
| Total columns | 14 |
| Duplicate records | 0 |
| Missing values | 0 |
| Random seed | 42 |

These figures describe the recorded dataset validation results. A fresh execution of the validation scripts is still required to confirm reproducibility.

### 2.4 Validation Implementation

The project includes automated dataset validation tests and a command-line validation workflow.

A FastAPI validation service was also developed to expose dataset validation functionality through API endpoints.

### 2.5 Limitations

The synthetic dataset is generated for project experimentation. Its distributions and observed relationships may not represent actual customer behaviour or commercial pricing environments.

The Hillstrom dataset is used separately for randomized email marketing treatment analysis and should not be treated as a real-world pricing experiment.

## 3. Causal Inference and Uplift Modelling

### 3.1 Hillstrom Dataset Analysis

The project uses the Hillstrom email marketing dataset, which contains approximately 64,000 customer records and 12 original columns.

The dataset supports randomized treatment analysis to study how different email marketing interventions influence customer purchasing behaviour.

The analysis includes:
- Comparing treatment and control groups.
- Calculating customer conversion rates.
- Measuring differences in purchase behaviour.
- Evaluating treatment effects.
- Examining statistical significance.

Previously recorded conversion rates:

| Group | Purchase Rate |
|---|---:|
| No Email | 0.573% |
| Men's Email | 1.253% |
| Women's Email | 0.884% |

The recorded differences compared with the No Email group were:
- Men's Email: +0.681 percentage points.
- Women's Email: +0.311 percentage points.

These are previously recorded analytical results and should be checked against the final reproducible analysis before submission.

### 3.2 Uplift Modelling

A T-Learner approach was implemented to estimate individual-level treatment effects.

The approach trains separate predictive models for treatment and control groups and estimates uplift by comparing their predictions.

The evaluation included:
- Predicted treatment effects.
- Observed average treatment effect (ATE).
- Qini coefficient.
- Uplift among the highest-ranked customer segment.

Previously recorded evaluation results:

| Metric | Recorded Result |
|---|---:|
| Qini coefficient | 0.8665 |
| Predicted mean uplift | Approximately +0.632 percentage points |
| Observed test ATE | Approximately +0.832 percentage points |
| Top 20% uplift | Approximately +1.313 percentage points |

The Qini coefficient evaluates uplift-ranking performance; it should not be described as classification accuracy.

### 3.3 Interpretation and Limitations

The Hillstrom dataset provides a randomized experimental setting for studying email marketing interventions.

However, email marketing treatment effects cannot automatically be generalized to price changes.

Uplift estimates are model-dependent and should be interpreted alongside the experimental design, evaluation methodology, and validation results.

## 4. Double Machine Learning (DML) Experiments

### 4.1 Overview

Double Machine Learning (DML) is used to estimate treatment effects while accounting for relationships between treatment assignment, outcomes, and other observed variables.

The project explores DML as part of its dynamic pricing causal analysis workflow.

The approach uses machine learning models to estimate nuisance functions and applies an orthogonalization procedure to reduce the impact of nuisance-model estimation errors on treatment-effect estimation.

### 4.2 Experimental Evaluation

The DML experiments included:
- Full-sample treatment-effect estimation.
- Holdout evaluation.
- Comparison between estimated and known treatment effects in synthetic experiments.
- Error measurement using MAE and RMSE.
- Model comparison and repeated-seed validation.

### 4.3 Previously Recorded Results

| Metric | Full Sample | Holdout |
|---|---:|---:|
| True ATE | 0.074463 | 0.074861 |
| Estimated ATE | 0.079521 | 0.092794 |
| MAE | 0.016636 | 0.020994 |
| RMSE | 0.020166 | 0.024203 |

These values are historical experiment results recorded during development. Their calculation, units, and reproducibility must be checked against the final DML implementation before submission.

### 4.4 Interpretation

The full-sample estimate is relatively close to the recorded true ATE.

The holdout estimate shows a larger difference from the true ATE, indicating that further evaluation is important.

MAE and RMSE measure estimation error in the experiment's outcome units. They should not be interpreted as percentages unless the underlying variables are explicitly defined that way.

### 4.5 Reproducibility Requirements

Before final submission, the following should be verified:

- Confirm the exact dataset and preprocessing steps used.
- Confirm the treatment and outcome variable definitions.
- Verify the train-test split and random seeds.
- Re-run the nuisance models and DML estimation.
- Confirm the MAE and RMSE calculations.
- Compare the results across repeated seeds.
- Document the model configuration and software dependencies.

### 4.6 Limitations

Synthetic DML experiments can compare estimated effects with known simulated effects. However, good performance on synthetic data does not establish that the same model will estimate real-world pricing effects accurately.

## 5. Dynamic Pricing and Policy Evaluation

### 5.1 Objective

The dynamic pricing component evaluates how different discount levels relate to customer purchasing behaviour and expected business outcomes.

The analysis uses the synthetic pricing dataset to compare pricing strategies and explore the trade-off between purchase conversion and profitability.

### 5.2 Discount-Level Analysis

The project evaluates five discount levels:

- 0% discount
- 5% discount
- 10% discount
- 15% discount
- 20% discount

Previously recorded API analysis results showed the following observed purchase rates:

| Discount Level | Observed Purchase Rate |
|---|---:|
| 0% | 20.65% |
| 5% | 21.18% |
| 10% | 26.74% |
| 15% | 31.19% |
| 20% | 34.49% |

These values represent observed group-level purchase rates in the synthetic dataset. They are not, by themselves, causal estimates of the effect of each discount.

### 5.3 Expected Profit Evaluation

A previously recorded policy comparison produced the following results:

| Discount Level | Expected Profit per Customer |
|---|---:|
| 0% | 33.24 |
| 5% | 33.42 |
| 10% | 32.85 |
| 15% | 31.41 |
| 20% | 28.93 |

In that recorded comparison, the 5% discount policy produced the highest expected profit per customer.

The currency unit and calculation assumptions should be confirmed from the original evaluation code and output before final submission.

### 5.4 Business Interpretation

The recorded results illustrate an important pricing trade-off:

- Higher discounts may be associated with higher purchase rates.
- Higher discounts can also increase discount costs.
- The discount level with the highest purchase rate may not produce the highest expected profit.
- Pricing decisions should consider profitability rather than conversion alone.

### 5.5 Analytical Limitations

The dataset is synthetic, so these findings demonstrate the analysis workflow rather than actual commercial performance.

The observed purchase rates and expected policy outcomes come from different analyses and should not be combined as though they were the same metric.

A final reproducibility check should verify the policy evaluation code, assumptions, and generated output files.

## 6. Backend API Development and Testing

### 6.1 Backend Overview

The project uses FastAPI to provide backend services for dataset validation and analytical metrics.

The backend is designed to support communication between the data analysis components and the interactive dashboard.

### 6.2 Dataset Validation API

A FastAPI validation service was developed to expose dataset validation functionality.

The validation workflow includes checks for:
- Missing or empty datasets.
- Required columns.
- Invalid data values.
- Numeric and non-finite values.
- Treatment and purchase indicator validity.
- Discount range constraints.

### 6.3 Overview Metrics API

An overview endpoint was implemented on the Fahma development branch:

**Endpoint:** `GET /api/overview`

The endpoint reads the synthetic pricing dataset and calculates:
- Total customer count.
- Overall purchase rate.
- Control and treated group counts.
- Purchase rates for both groups.
- Observed difference in purchase rates.
- Purchase rates by discount level.
- Total revenue.
- Total discount cost.

The response also includes a warning that the dataset is synthetic and that the results do not establish real-world pricing effectiveness.

### 6.4 API Testing

Previously recorded testing results include:

| Test Area | Recorded Result |
|---|---|
| Dataset validation API tests | 5 passed |
| Overview API tests | 4 passed |
| Full test suite | 28 passed |
| Overview endpoint with synthetic dataset | HTTP 200 |
| Missing dataset handling | Tested |
| Missing required columns | Tested |
| Invalid purchase values | Tested |

These are historical development results and should be confirmed by running the current test suite before final submission.

### 6.5 API Implementation and Reliability

The implementation includes error handling for missing datasets and invalid input conditions.

Automated tests help verify expected endpoint behaviour and reduce the risk of incorrect analytical responses.

### 6.6 Branch and Integration Considerations

Backend development has taken place across separate team branches.

The Fahma branch contains the dataset validation service and overview metrics endpoint. Hiba's branch contains separate dashboard and backend integration work.

These implementations must be reviewed and coordinated before final integration. Their endpoints, data formats, dependencies, and file paths should be checked for compatibility.

### 6.7 Remaining Verification

Before submission:
- Re-run all backend tests.
- Verify all API endpoints.
- Check API response structures.
- Confirm dataset paths and required files.
- Review error handling.
- Test frontend-to-backend communication after integration.

## 7. Frontend Dashboard Development and Integration

### 7.1 Dashboard Overview

The project includes an interactive dashboard developed using Next.js, React, TypeScript, and Tailwind CSS.

The dashboard is designed to present pricing analysis, causal inference results, uplift modelling insights, and model evaluation information in an accessible format.

### 7.2 Dashboard Modules

The reported dashboard structure includes the following modules:

- **Overview:** Displays important project metrics and analytical summaries.
- **Pricing Analytics:** Presents discount-level analysis and pricing-related results.
- **Causal Analysis:** Displays treatment-effect analysis.
- **Uplift Analysis:** Presents customer uplift modelling results.
- **Model Insights:** Provides information about model performance and evaluation.

Additional reported features include:
- Interactive charts and metric cards.
- Global search functionality.
- Dynamic data loading.
- Report export functionality.

### 7.3 Backend Integration

The Hiba development branch contains reported dashboard and FastAPI backend integration work.

The reported backend endpoints include:

- `/api/health`
- `/api/pricing`
- `/api/causal`
- `/api/uplift`
- `/api/model-insights`
- `/api/overview`
- `/api/report`

The dashboard is intended to retrieve analytical information through these API endpoints.

### 7.4 Reported Testing Status

Previous team updates reported:
- Backend API routes returning HTTP 200.
- Frontend production build passing.
- Syntax checks passing.
- Manual dashboard checks completed.
- Report export functionality tested.

These results are based on development updates and still require independent verification against the latest repository state.

### 7.5 Branch Coordination

Frontend and backend development have been maintained across separate Git branches.

The Hiba branch contains the dashboard integration work, while the Fahma branch contains separate data validation, API, testing, and analytical documentation work.

The branches should be reviewed together before final integration. Existing functionality must be preserved during any merge or deployment preparation.

### 7.6 Remaining Integration Checks

Before submission:
- Confirm that the frontend uses the correct backend endpoints.
- Verify request and response formats.
- Check environment variables and API base URLs.
- Confirm that all dashboard modules display the correct data.
- Test report export.
- Verify production build and deployment configuration.
- Confirm that the integrated application works from a clean setup.

## 8. Reproducibility, Dependencies and Execution

### 8.1 Reproducibility Objective

Reproducibility ensures that the project's analytical results, model evaluations, and backend services can be executed again under documented conditions.

The project uses Python-based data analysis, machine learning, automated testing, and API development tools.

### 8.2 Development Environment

The development environment includes:

- Python 3.13.5 (used in the current local virtual environment).
- Visual Studio Code.
- Git and GitHub for version control.
- FastAPI for backend API development.
- Uvicorn for running the API server.
- Pandas and NumPy for data processing.
- Machine learning libraries for model development.
- Next.js, React, TypeScript, and Tailwind CSS for the dashboard.

The complete dependency list and exact package versions must be verified against the project's dependency files.

### 8.3 Reproducibility Requirements

The following practices are important for reproducing the results:

1. Use the correct project Python environment.
2. Install dependencies from the documented dependency file.
3. Keep dataset paths consistent.
4. Record random seeds used during synthetic data generation and model experiments.
5. Follow the documented preprocessing steps.
6. Execute the analysis and evaluation scripts in the correct order.
7. Run automated tests after setup.
8. Verify generated reports and API responses.

### 8.4 Dataset and Model Availability

The synthetic pricing dataset is used by the analytical and API components.

The availability of all required datasets, trained model files, and generated reports must be checked before a fresh setup or deployment.

The Hillstrom dataset and other external data files should have clearly documented download or setup instructions if they are required to reproduce particular experiments.

### 8.5 Execution Verification

A clean-environment execution check is still required to establish that another user can install the dependencies and run the project without relying on files or packages available only on the original development machine.

### 8.6 Reproducibility Limitations

Previous successful runs demonstrate development progress, but they do not automatically guarantee reproducibility on another computer.

The final documentation should include verified installation commands, execution commands, dataset requirements, environment variables, and expected outputs.

## 9. Known Limitations and Pending Tasks

### 9.1 Data Limitations

- The synthetic pricing dataset does not represent actual commercial customer behaviour.
- Pricing results should be interpreted as experimental demonstrations.
- The Hillstrom dataset focuses on email marketing interventions rather than pricing treatments.
- Results from one experimental setting should not automatically be generalized to another.

### 9.2 Model Limitations

- DML estimates require further reproducibility and holdout validation.
- Uplift performance depends on the selected models, data preparation, and evaluation methodology.
- Model performance metrics should be interpreted according to their definitions.
- Further validation is needed before applying the models to real business decisions.

### 9.3 Backend and Frontend Limitations

- Separate branch implementations require final compatibility checks.
- API endpoint behaviour must be verified against the integrated dashboard.
- Deployment configuration and environment variables require final review.
- Clean-environment installation and execution have not yet been fully verified.

### 9.4 Pending Development Tasks

The following activities remain important before final submission:

1. Audit the original Infotact Project 2 requirements.
2. Verify the current repository structure and branch contents.
3. Re-run dataset validation.
4. Reproduce the DML experiment results.
5. Reproduce the uplift modelling results.
6. Verify dynamic pricing policy calculations.
7. Run the complete automated test suite.
8. Review all backend API endpoints.
9. Test frontend and backend integration.
10. Verify dependency installation and execution instructions.
11. Review the README and technical documentation.
12. Perform final deployment and submission checks.

### 9.5 Submission Readiness

The project has made progress across data analysis, causal inference, machine learning, backend development, testing, and dashboard implementation.

However, the original project requirements audit, independent reproducibility checks, and final integration verification remain necessary.

Therefore, the project should not yet be considered fully submission-ready.

## 10. Final Validation Checklist and Conclusion

### 10.1 Final Validation Checklist

The following checklist should be completed before project submission.

| Task | Status |
|---|---|
| Project objective documented | Completed |
| Synthetic pricing dataset analysis documented | Completed |
| Dataset validation workflow documented | Completed |
| Hillstrom analysis documented | Completed |
| Uplift modelling results documented | Completed |
| DML experiment results documented | Completed |
| Dynamic pricing analysis documented | Completed |
| Backend API development documented | Completed |
| Frontend dashboard work documented | Completed |
| Full original requirements audit | Pending |
| Fresh dataset validation execution | Pending |
| DML reproducibility verification | Pending |
| Uplift results reproducibility verification | Pending |
| Full automated test execution | Pending |
| Frontend-backend integration verification | Pending |
| Clean-environment setup verification | Pending |
| Final deployment verification | Pending |

**Note:** "Completed" in this table means documented in this report. It does not independently certify that the underlying implementation has passed final verification.

### 10.2 Conclusion

EconoCausal – Dynamic Pricing via Double Machine Learning is an integrated data science project exploring customer treatment effects, uplift modelling, and dynamic pricing analysis.

The project combines experimental data analysis, synthetic pricing experiments, machine learning techniques, causal inference methods, automated validation, FastAPI backend services, and an interactive dashboard.

The development work establishes a foundation for evaluating pricing strategies and understanding customer responses through data-driven methods.

Further reproducibility testing, technical verification, branch integration, and requirement-based review are necessary before the final submission.

### 10.3 Next Development Phase

The next development phase will focus on:

- Completing the original Infotact requirements audit.
- Reproducing the analytical results.
- Verifying the integrated application.
- Resolving any identified issues.
- Finalizing technical documentation.
- Preparing the project for deployment and submission.

---

**Report:** Project Reproducibility and Validation Review  
**Project:** EconoCausal – Dynamic Pricing via Double Machine Learning  
**Document Type:** Technical Progress and Validation Review

## 11. Week 4 Deliverables and Project Deployment

### 11.1 Week 4 Documentation

The Week 4 project write-up was completed as part of the project documentation and progress submission.

### 11.2 Application Deployment

The EconoCausal application was deployed using Streamlit Community Cloud.

**Live Application:**

https://econocausal-dynamic-pricing-gfdrwm7ks23fdwnjzlnu4v.streamlit.app/

The deployment provides a hosted version of the project for application access and demonstration.

### 11.3 Project Presentation

A PowerPoint presentation was also created to communicate the project objective, methodology, implementation, analytical findings, and project outcomes.

### 11.4 Week 4 Milestone Summary

The following deliverables were completed:

- Week 4 project write-up.
- Application deployment on Streamlit Community Cloud.
- PowerPoint presentation creation.
- Reproducibility and validation review report draft.

### 11.5 Deployment Verification

The deployed application URL has been recorded. A final manual check is still required to verify application accessibility, functionality, and consistency with the latest repository version.