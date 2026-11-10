
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path

API_BASE = "https://econocausal-dynamic-pricing.onrender.com"

st.set_page_config(
    page_title="EconoCausal | Dynamic Pricing",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .main {background-color: #f7f9fc;}
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}
    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #e5eaf2;
        padding: 16px;
        border-radius: 12px;
    }
    section[data-testid="stSidebar"] {
        background-color: #101c35;
    }
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    .subtitle {color: #64748b; font-size: 15px;}
    .section-note {
        background: #eef4ff;
        padding: 12px 16px;
        border-radius: 8px;
        color: #334155;
        margin: 10px 0 20px 0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=60, show_spinner=False)
def fetch_json(endpoint):
    response = requests.get(
        f"{API_BASE}/api/{endpoint}",
        timeout=120
    )
    response.raise_for_status()
    return response.json()


@st.cache_data(show_spinner=False)
def load_hillstrom_data():
    data_path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "hillstrom.csv"
    )

    if not data_path.exists():
        raise FileNotFoundError(
            "Hillstrom dataset not found in the data folder."
        )

    return pd.read_csv(data_path)


def show_error(error):
    st.error(f"Could not load data from the backend: {error}")
    st.info(
        "The Render free service may be waking up. "
        "Wait a little and use Refresh Data to try again."
    )


def metric_row(items):
    columns = st.columns(len(items))
    for column, (label, value, help_text) in zip(columns, items):
        column.metric(label, value, help=help_text)


def show_disclaimer(message):
    if message:
        st.caption(f"Note: {message}")


# SIDEBAR
with st.sidebar:
    st.title("📊 EconoCausal")
    st.caption("Dynamic Pricing via Double Machine Learning")
    st.divider()

    page = st.radio(
        "DASHBOARD",
        [
            "Overview",
            "Pricing Analytics",
            "Causal Analysis",
            "Uplift Analysis",
            "Model Insights",
            "Data Explorer",
        ],
    )

    st.divider()

    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.caption("Live data from the deployed API")
    st.caption("Team Dashboard | 2026")


# HEADER
st.title("EconoCausal Dashboard")
st.markdown(
    '<p class="subtitle">Causal analysis, uplift modelling and '
    'data-driven dynamic pricing</p>',
    unsafe_allow_html=True,
)

st.divider()


# OVERVIEW
if page == "Overview":
    try:
        data = fetch_json("overview")

        st.subheader("Project Overview")
        st.write(
            "A data-driven dashboard combining causal inference, "
            "uplift modelling and dynamic pricing analysis."
        )

        metric_row([
            ("Customers Analysed", f'{data["customers_analysed"]:,}', None),
            ("Best Tested Discount", data["best_discount"], None),
            ("Expected Profit / Customer",
             f'{data["expected_profit_per_customer"]:.2f}', None),
            ("Qini Coefficient", f'{data["qini_coefficient"]:.4f}',
             "Measures uplift ranking quality."),
        ])

        st.subheader("Key Results")
        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Men's Email Treatment Effect",
                f'{data["mens_email_effect"]:.3f} pp',
                help="Effect compared with the randomized No Email group.",
            )

        with col2:
            st.metric(
                "Pricing Dataset Customers",
                f'{data["pricing_dataset_customers"]:,}',
            )

        st.metric(
            "DML Holdout Estimated ATE",
            f'{data["dml_holdout_ate"]:.4f}',
        )

        st.subheader("Data Sources")
        for source in data["data_sources"]:
            st.write(f"• {source}")

        st.info(
            "The project uses a randomized email experiment and a "
            "separate synthetic pricing dataset. Synthetic results "
            "should not be interpreted as proven real-world outcomes."
        )

    except Exception as error:
        show_error(error)


# PRICING ANALYTICS
elif page == "Pricing Analytics":
    try:
        data = fetch_json("pricing")
        policies = pd.DataFrame(data["policies"])
        effects = pd.DataFrame(data["causal_effects"])

        st.subheader("Pricing Policy Performance")
        st.caption(
            f'Dataset: {data["dataset"]} | '
            f'{data["customers"]:,} customers'
        )

        best = data["best_policy"]
        metric_row([
            ("Best Discount", best["discount"], None),
            ("Purchase Rate", f'{best["purchase_rate"]:.2f}%', None),
            ("Profit / Customer", f'{best["profit"]:.2f}', None),
            ("Total Profit", f'{best["total_profit"]:,.2f}', None),
        ])

        st.subheader("Compare Discount Policies")
        selected_metrics = st.selectbox(
            "Choose a metric",
            ["profit", "revenue", "purchase_rate"],
            format_func=lambda x: {
                "profit": "Profit per customer",
                "revenue": "Revenue per customer",
                "purchase_rate": "Purchase rate (%)",
            }[x],
        )

        fig = px.bar(
            policies,
            x="discount",
            y=selected_metrics,
            color="discount",
            text_auto=".2f",
            title="Performance across discount levels",
            labels={
                "discount": "Discount",
                selected_metrics: selected_metrics.replace("_", " ").title(),
            },
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Policy Comparison Table")
        st.dataframe(
            policies[
                [
                    "discount",
                    "purchase_rate",
                    "revenue",
                    "profit",
                    "total_revenue",
                    "total_profit",
                ]
            ].rename(columns={
                "discount": "Discount",
                "purchase_rate": "Purchase Rate (%)",
                "revenue": "Revenue / Customer",
                "profit": "Profit / Customer",
                "total_revenue": "Total Revenue",
                "total_profit": "Total Profit",
            }),
            use_container_width=True,
            hide_index=True,
        )

        st.subheader("Causal Effect Estimation by Discount")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=effects["discount"],
            y=effects["true_ate"],
            name="True ATE",
        ))
        fig.add_trace(go.Bar(
            x=effects["discount"],
            y=effects["estimated_ate"],
            name="Estimated ATE",
        ))
        fig.update_layout(
            barmode="group",
            xaxis_title="Discount",
            yaxis_title="Treatment effect",
        )
        st.plotly_chart(fig, use_container_width=True)

        show_disclaimer(data.get("disclaimer"))

    except Exception as error:
        show_error(error)


# CAUSAL ANALYSIS
elif page == "Causal Analysis":
    try:
        data = fetch_json("causal")
        effects = pd.DataFrame(data["effects"])
        segments = pd.DataFrame(data["segment_counts"])

        st.subheader("Randomized Email Experiment")
        st.caption(
            f'{data["dataset"]} | {data["customers"]:,} customers'
        )

        st.write(f'Control group: **{data["control_group"]}**')

        st.subheader("Customer Distribution")
        fig = px.pie(
            segments,
            names="name",
            values="value",
            hole=0.45,
            title="Customers in each experimental group",
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Treatment Effects")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=effects["segment"],
            y=effects["effect"],
            name="Estimated effect",
            error_y=dict(
                type="data",
                symmetric=False,
                array=effects["upper"] - effects["effect"],
                arrayminus=effects["effect"] - effects["lower"],
            ),
        ))
        fig.update_layout(
            yaxis_title="Effect (percentage points)",
            xaxis_title="Email treatment group",
            title="Treatment effect with 95% confidence intervals",
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Statistical Results")
        display = effects[
            [
                "segment",
                "effect",
                "lower",
                "upper",
                "p_value",
                "z_score",
                "treatment_conversion_rate",
                "control_conversion_rate",
            ]
        ].copy()

        display.columns = [
            "Treatment Group",
            "Effect (pp)",
            "CI Lower",
            "CI Upper",
            "P-value",
            "Z-score",
            "Treatment Conversion (%)",
            "Control Conversion (%)",
        ]
        st.dataframe(display, use_container_width=True, hide_index=True)

        st.info(data["explanation"])
        st.caption(
            "The confidence intervals show the uncertainty around "
            "the estimated treatment effects."
        )

    except Exception as error:
        show_error(error)


# UPLIFT ANALYSIS
elif page == "Uplift Analysis":
    try:
        data = fetch_json("uplift")
        metrics = data["metrics"]

        st.subheader("Uplift Modelling")
        st.write(f'Model: **{data["model"]}**')
        st.caption(data["model_type"])

        metric_row([
            ("Qini Coefficient", f'{metrics["qini_coefficient"]:.4f}', None),
            ("Predicted Mean Uplift",
             f'{metrics["predicted_mean_uplift"]:.3f} pp', None),
            ("Observed Test ATE",
             f'{metrics["observed_test_ate"]:.3f} pp', None),
            ("Top 20% Uplift",
             f'{metrics["top_20_percent_uplift"]:.3f} pp', None),
        ])

        st.subheader("Model Evaluation Metrics")
        metric_row([
            ("ROC-AUC", f'{metrics["roc_auc"]:.4f}', None),
            ("PR-AUC", f'{metrics["pr_auc"]:.4f}', None),
        ])

        comparison = pd.DataFrame({
            "Metric": [
                "Predicted Mean Uplift",
                "Observed Test ATE",
                "Top 20% Uplift",
            ],
            "Value (percentage points)": [
                metrics["predicted_mean_uplift"],
                metrics["observed_test_ate"],
                metrics["top_20_percent_uplift"],
            ],
        })

        fig = px.bar(
            comparison,
            x="Metric",
            y="Value (percentage points)",
            color="Metric",
            text_auto=".3f",
            title="Uplift comparison",
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        st.info(data["qini_explanation"])
        st.caption(data["source"])

    except Exception as error:
        show_error(error)


# MODEL INSIGHTS
elif page == "Model Insights":
    try:
        data = fetch_json("model-insights")
        primary = data["primary_validation"]

        st.subheader("Double Machine Learning Validation")
        st.caption(data["dataset"])

        metric_row([
            ("Holdout Customers", f'{primary["holdout_customers"]:,}', None),
            ("True ATE", f'{primary["true_ate"]:.5f}', None),
            ("Estimated ATE", f'{primary["estimated_ate"]:.5f}', None),
            ("Effect Correlation",
             f'{primary["effect_correlation"]:.4f}', None),
        ])

        metric_row([
            ("ATE Bias", f'{primary["ate_bias"]:.5f}', None),
            ("MAE", f'{primary["mae"]:.5f}', None),
            ("RMSE", f'{primary["rmse"]:.5f}', None),
        ])

        st.subheader("Estimator Comparison")
        estimator = pd.DataFrame(data["estimator_comparison"])
        st.dataframe(estimator, use_container_width=True, hide_index=True)

        fig = px.bar(
            estimator,
            x="estimator",
            y=["mae", "rmse"],
            barmode="group",
            title="Prediction error by estimator",
            labels={
                "estimator": "Estimator",
                "value": "Error",
                "variable": "Metric",
            },
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Repeated Seed Validation")
        repeated = pd.DataFrame(data["repeated_seed_summary"])
        st.dataframe(repeated, use_container_width=True, hide_index=True)

        st.subheader("Train-Test Split Validation")
        split = pd.DataFrame(data["split_ratio_validation"])
        fig = px.line(
            split,
            x="training_percentage",
            y=["mae", "rmse"],
            markers=True,
            title="Model error across training split ratios",
            labels={
                "training_percentage": "Training data (%)",
                "value": "Error",
                "variable": "Metric",
            },
        )
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(split, use_container_width=True, hide_index=True)

        st.subheader("Model Configuration Comparison")
        config = pd.DataFrame(data["configuration_summary"])
        st.dataframe(config, use_container_width=True, hide_index=True)

        st.info(
            "These validation results measure performance on the "
            "synthetic pricing validation dataset. They do not prove "
            "real-world causal effects."
        )
        show_disclaimer(data.get("disclaimer"))

    except Exception as error:
        show_error(error)


# DATA EXPLORER
elif page == "Data Explorer":

    st.subheader("Data Explorer")
    st.write(
        "Search existing customer records and upload "
        "new CSV datasets for inspection."
    )

    # CUSTOMER SEARCH
    st.divider()
    st.subheader("1. Search Customer Records")

    try:
        existing_df = load_hillstrom_data()

        st.caption(
            f"Hillstrom Dataset | {len(existing_df):,} records"
        )

        search_text = st.text_input(
            "🔍 Search customer details",
            placeholder="Search by segment, channel, recency, etc."
        )

        results = existing_df.copy()

        if search_text.strip():
            mask = results.astype(str).apply(
                lambda column: column.str.contains(
                    search_text,
                    case=False,
                    na=False,
                    regex=False
                )
            ).any(axis=1)

            results = results.loc[mask]

        st.write(f"Matching records: {len(results):,}")

        if not results.empty:

            display_results = results.copy()
            display_results.insert(
                0,
                "Record Number",
                results.index + 1
            )

            st.dataframe(
                display_results.head(200),
                use_container_width=True,
                hide_index=True
            )

            selected_record = st.selectbox(
                "Select a record to see complete details",
                results.index.tolist(),
                format_func=lambda x: f"Record {x + 1}"
            )

            st.subheader("Individual Customer Details")

            st.dataframe(
                results.loc[selected_record].rename(
                    "Customer Details"
                ).to_frame(),
                use_container_width=True
            )

        else:
            st.warning("No matching records found.")

    except Exception as error:
        show_error(error)

    # CSV UPLOAD
    st.divider()
    st.subheader("2. Upload a New Dataset")

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:

        try:
            uploaded_df = pd.read_csv(uploaded_file)

            if uploaded_df.empty:
                st.error("The uploaded CSV contains no records.")

            else:
                st.success("CSV uploaded and read successfully.")

                st.subheader("Uploaded Dataset Summary")

                metric_row([
                    ("Total Records", f"{len(uploaded_df):,}", None),
                    ("Total Columns", f"{len(uploaded_df.columns):,}", None),
                    (
                        "Missing Values",
                        f"{uploaded_df.isna().sum().sum():,}",
                        None
                    ),
                    (
                        "Duplicate Rows",
                        f"{uploaded_df.duplicated().sum():,}",
                        None
                    ),
                ])

                st.subheader("Column Information")

                column_info = pd.DataFrame({
                    "Column": uploaded_df.columns,
                    "Data Type": uploaded_df.dtypes.astype(str).values,
                    "Missing Values": uploaded_df.isna().sum().values,
                })

                st.dataframe(
                    column_info,
                    use_container_width=True,
                    hide_index=True
                )

                if uploaded_df.columns.duplicated().any():
                    st.warning("Duplicate column names detected.")

                if uploaded_df.isna().sum().sum() > 0:
                    st.warning(
                        "Missing values detected. "
                        "Review the dataset before analysis."
                    )
                else:
                    st.success("No missing values detected.")

                if uploaded_df.duplicated().sum() > 0:
                    st.warning("Duplicate records detected.")

                st.subheader("Dataset Preview")

                st.dataframe(
                    uploaded_df.head(100),
                    use_container_width=True,
                    hide_index=True
                )

                st.download_button(
                    "Download Uploaded CSV",
                    data=uploaded_file.getvalue(),
                    file_name=uploaded_file.name,
                    mime="text/csv"
                )

        except Exception as error:
            st.error(f"Unable to process CSV: {error}")

    st.info(
        "Uploaded datasets are currently used for preview "
        "and basic validation only. They do not modify the "
        "existing pricing models or dashboard results."
    )


# REPORT DOWNLOAD
st.divider()
st.subheader("Project Report")

st.write(
    "Download the report generated by the deployed backend."
)

try:
    report_response = requests.get(
        f"{API_BASE}/api/report",
        timeout=120,
    )
    report_response.raise_for_status()

    st.download_button(
        label="📥 Download Project Report",
        data=report_response.content,
        file_name="EconoCausal_Project_Report.txt",
        mime="text/plain",
    )
except Exception:
    st.warning(
        "The report is temporarily unavailable. "
        "Please try again later."
    )


st.divider()
st.caption(
    "EconoCausal: Dynamic Pricing via Double Machine Learning | "
    "Academic project dashboard"
)
