import streamlit as st
import pandas as pd
import plotly.express as px
from validator import validate_data

st.set_page_config(
    page_title="AI Data Quality Validator",
    layout="wide"
)

st.title("🚀 AI Data Quality Validator")

st.markdown("""
Upload CSV files and automatically detect:
- Missing values
- Duplicate rows
- Invalid emails
- Invalid phone numbers
- Suspicious records
""")

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Uploaded Data")

    st.dataframe(df, use_container_width=True)

    report = validate_data(df)

    # -------------------------
    # HEALTH SCORE
    # -------------------------

    total_issues = (
        sum(report["missing_values"].values())
        + report["duplicate_rows"]
        + len(report["invalid_emails"])
        + len(report["invalid_phones"])
        + report["suspicious_salary_count"]
    )

    total_cells = df.shape[0] * df.shape[1]

    health_score = max(
        0,
        round(100 - ((total_issues / total_cells) * 100))
    )

    st.subheader("📊 Data Health Score")

    st.progress(health_score / 100)

    st.metric(
        label="Overall Data Quality Score",
        value=f"{health_score}%"
    )

    # -------------------------
    # METRICS
    # -------------------------

    st.subheader("📌 Validation Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Duplicate Rows",
        report["duplicate_rows"]
    )

    col2.metric(
        "Invalid Emails",
        len(report["invalid_emails"])
    )

    col3.metric(
        "Invalid Phones",
        len(report["invalid_phones"])
    )

    col4.metric(
        "Suspicious Salaries",
        report["suspicious_salary_count"]
    )

    # -------------------------
    # CHARTS
    # -------------------------

    st.subheader("📈 Data Quality Charts")

    chart_data = pd.DataFrame({
        "Issue Type": [
            "Duplicates",
            "Invalid Emails",
            "Invalid Phones",
            "Suspicious Salaries"
        ],
        "Count": [
            report["duplicate_rows"],
            len(report["invalid_emails"]),
            len(report["invalid_phones"]),
            report["suspicious_salary_count"]
        ]
    })

    fig = px.bar(
        chart_data,
        x="Issue Type",
        y="Count",
        title="Detected Data Issues"
    )

    st.plotly_chart(fig, use_container_width=True)

    # -------------------------
    # MISSING VALUES
    # -------------------------

    st.subheader("❌ Missing Values")

    missing_df = pd.DataFrame(
        list(report["missing_values"].items()),
        columns=["Column", "Missing Count"]
    )

    st.dataframe(missing_df)

    # -------------------------
    # INVALID EMAILS
    # -------------------------

    st.subheader("📧 Invalid Emails")

    st.write(report["invalid_emails"])

    # -------------------------
    # INVALID PHONES
    # -------------------------

    st.subheader("📱 Invalid Phone Numbers")

    st.write(report["invalid_phones"])

    # -------------------------
    # CLEAN DATA
    # -------------------------

    cleaned_df = df.drop_duplicates()

    cleaned_df = cleaned_df.dropna()

    # remove invalid emails
    cleaned_df = cleaned_df[
        cleaned_df["email"].str.contains(
            r'^[\w\.-]+@[\w\.-]+\.\w+$',
            regex=True,
            na=False
        )
    ]

    # -------------------------
    # DOWNLOAD BUTTON
    # -------------------------

    csv = cleaned_df.to_csv(index=False)

    st.download_button(
        label="⬇ Download Cleaned CSV",
        data=csv,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )

    # -------------------------
    # RISK SUMMARY
    # -------------------------

    st.subheader("⚠ Risk Summary")

    risks = []

    if report["duplicate_rows"] > 0:
        risks.append("High: Duplicate records detected")

    if len(report["invalid_emails"]) > 0:
        risks.append("Medium: Invalid email formats found")

    if len(report["invalid_phones"]) > 0:
        risks.append("Medium: Invalid phone numbers found")

    if report["suspicious_salary_count"] > 0:
        risks.append("High: Suspicious salary values detected")

    if len(risks) == 0:
        st.success("No major data quality issues detected")
    else:
        for risk in risks:
            st.warning(risk)