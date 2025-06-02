# salary_analysis_app.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import numpy as np
from fpdf import FPDF
import tempfile
import os

st.set_page_config(page_title="Salary Analysis App", layout="wide")
st.title("📊 Advanced Salary Analysis")

# File upload
uploaded_file = st.file_uploader("📤 Upload your cleaned salary dataset (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📋 Dataset Overview")
    st.dataframe(df.head())

    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    selected_gender = st.sidebar.multiselect("Filter by Gender", options=df["Gender"].unique(), default=df["Gender"].unique())
    selected_department = st.sidebar.multiselect("Filter by Department", options=df["Department"].unique(), default=df["Department"].unique())

    filtered_df = df[(df["Gender"].isin(selected_gender)) & (df["Department"].isin(selected_department))]

    st.subheader("📊 Scatter Plot with Linear Regression")
    x_axis = st.selectbox("Choose the X-axis", ["Age", "Experience (years)"])
    y_axis = "Salary (R$)"

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.scatterplot(data=filtered_df, x=x_axis, y=y_axis, hue="Gender", palette="Set2", alpha=0.7, ax=ax)

    # Regression line
    X = filtered_df[[x_axis]]
    y = filtered_df[y_axis]
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)

    ax.plot(X, y_pred, color='red', label='Linear Regression')
    ax.legend()
    st.pyplot(fig)

    slope = model.coef_[0]
    intercept = model.intercept_
    r2 = r2_score(y, y_pred)

    st.markdown("### 📈 Regression Summary")
    st.markdown(f"- **Intercept:** R$ {intercept:.2f}")
    st.markdown(f"- **Slope:** R$ {slope:.2f} per unit of {x_axis}")
    st.markdown(f"- **R² Score:** {r2:.4f} ({r2*100:.2f}% of salary variance explained)")

    st.markdown("---")
    st.subheader("📚 Multiple Linear Regression")
    st.markdown("Predict salary using **Age**, **Experience**, and **Education**")

    # Convert categorical to dummy variables
    df_encoded = pd.get_dummies(filtered_df, columns=["Education"], drop_first=True)
    predictors = ["Age", "Experience (years)"] + [col for col in df_encoded.columns if col.startswith("Education_")]

    X_multi = df_encoded[predictors]
    y_multi = df_encoded[y_axis]
    multi_model = LinearRegression()
    multi_model.fit(X_multi, y_multi)
    y_multi_pred = multi_model.predict(X_multi)
    r2_multi = r2_score(y_multi, y_multi_pred)

    st.markdown(f"- **Predictors used:** {', '.join(predictors)}")
    st.markdown(f"- **R² Score (Multiple Regression):** {r2_multi:.4f} ({r2_multi*100:.2f}% of salary variance explained)")

    st.markdown("#### Coefficients")
    coef_text = []
    for feature, coef in zip(predictors, multi_model.coef_):
        st.markdown(f"- {feature}: R$ {coef:.2f}")
        coef_text.append(f"{feature}: R$ {coef:.2f}")

    # Export PDF
    st.markdown("---")
    st.subheader("📤 Export Report to PDF")

    if st.button("Generate PDF Report"):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Save plot as image
            plot_path = os.path.join(tmpdir, "regression_plot.png")
            fig.savefig(plot_path)

            # Create PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            pdf.cell(200, 10, txt="Salary Analysis Report", ln=1, align='C')
            pdf.ln(10)

            pdf.cell(200, 10, txt=f"Simple Linear Regression (X = {x_axis})", ln=1)
            pdf.cell(200, 10, txt=f"Intercept: R$ {intercept:.2f}", ln=1)
            pdf.cell(200, 10, txt=f"Slope: R$ {slope:.2f} per {x_axis}", ln=1)
            pdf.cell(200, 10, txt=f"R² Score: {r2:.4f}", ln=1)
            pdf.ln(10)

            pdf.cell(200, 10, txt="Multiple Linear Regression:", ln=1)
            pdf.cell(200, 10, txt=f"R² Score: {r2_multi:.4f}", ln=1)
            for line in coef_text:
                pdf.cell(200, 10, txt=line, ln=1)

            # Insert plot
            pdf.image(plot_path, x=10, y=None, w=180)

            output_path = os.path.join(tmpdir, "salary_analysis_report.pdf")
            pdf.output(output_path)

            with open(output_path, "rb") as f:
                st.download_button("📄 Download PDF Report", f, file_name="salary_analysis_report.pdf")
else:
    st.info("Please upload a CSV file to begin.")
