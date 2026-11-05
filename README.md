# EconoCausal - Dynamic Pricing via Double Machine Learning



## 1. Project Overview



EconoCausal is a data science project focused on understanding causal effects and applying Double Machine Learning (DML) to dynamic pricing problems.



The project explores how treatment effects can support data-driven pricing and discount decisions.



## 2. Project Objectives



\- Understand causal relationships in pricing decisions.

\- Explore experimental and observational datasets.

\- Estimate treatment effects using causal inference methods.

\- Develop and evaluate dynamic pricing approaches.

\- Validate pricing data and improve model reliability.



## 3. Dataset Components



The project explores three datasets:



### Hillstrom Dataset

Used for exploratory analysis of randomized marketing experiments and customer treatment effects.



### UCI Online Retail Dataset

Used for observational retail data exploration. Its observational nature must be considered when interpreting causal relationships.



### Synthetic Pricing Dataset

Used to investigate pricing and discount treatment effects under controlled assumptions.



## 4. Methodology



\- Data preprocessing and validation

\- Exploratory Data Analysis

\- Causal problem formulation

\- Double Machine Learning

\- Treatment effect estimation

\- Model evaluation and robustness analysis

\- Dynamic pricing analysis



## 5. Repository Structure



```text

EconoCausal-Dynamic-Pricing/

â”œâ”€â”€ docs/

â”œâ”€â”€ reports/

â”œâ”€â”€ src/

â”‚   â””â”€â”€ data\_processing/

â”‚       â””â”€â”€ validate\_pricing\_data.py

â”œâ”€â”€ tests/

â”‚   â””â”€â”€ test\_validate\_pricing\_data.py

â”œâ”€â”€ requirements.txt

â””â”€â”€ README.md

```



## 6. Installation



Clone the repository:



```bash

git clone https://github.com/fahmaparveen3-arch/EconoCausal-Dynamic-Pricing.git

cd EconoCausal-Dynamic-Pricing

```



Install dependencies:



```bash

pip install -r requirements.txt

```



## 7. Running Tests



```bash

python -m pytest tests/ -v

```



The Afnan branch currently contains 10 pricing data validation tests. All 10 passed in the latest verified run.



## 8. Important Limitations



\- Hillstrom results relate to a randomized marketing experiment.

\- Online Retail data is observational and does not independently establish causal effects.

\- Synthetic pricing results depend on the assumptions used to generate the data.

\- Model estimates should be interpreted with appropriate validation and uncertainty analysis.



## 9. Documentation



Refer to the `docs/` and `reports/` directories for causal analysis, dataset research, methodology, validation and project findings.
