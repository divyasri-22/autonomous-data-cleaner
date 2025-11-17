import streamlit as st
import pandas as pd
from pathlib import Path

from schema_report import generate_schema_report
from rule_suggestions import generate_rule_suggestions
from auto_cleaner import auto_clean_file

# ---- BASIC PAGE CONFIG ----
st.set_page_config(
    page_title="Autonomous Data Cleaner",
    layout="wide",
)

st.title("🤖 Autonomous Data Cleaning & Schema Understanding Agent")

st.markdown(
    "Upload any **CSV** file and this app will:\n"
    "1. Profile the schema\n"
    "2. Suggest cleaning rules\n"
    "3. Apply automatic cleaning and show the cleaned data"
)

# ---- FILE UPLOAD ----
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # Save to your project /data folder
    project_root = Path(__file__).resolve().parents[1]  # .. from src
    data_dir = project_root / "data"
    data_dir.mkdir(exist_ok=True)

    raw_path = data_dir / "uploaded_raw.csv"
    with open(raw_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Load dataframe
    df = pd.read_csv(raw_path)

    st.subheader("Raw Data Preview")
    max_preview = min(len(df), 100)
    n_rows = st.slider(
        "Number of rows to preview",
        min_value=5,
        max_value=int(max_preview),
        value=10,
        step=5,
    )
    st.dataframe(df.head(n_rows))

    # ---- RUN PIPELINE BUTTON ----
    if st.button("🚀 Run Autonomous Cleaning Pipeline"):
        with st.spinner("Running schema analysis and cleaning..."):

            # 1. Schema report
            schema_df, schema_path = generate_schema_report(str(raw_path))

            # 2. Rule suggestions (no printing, just return list)
            suggestions, suggestions_path = generate_rule_suggestions(df, str(raw_path))

            # 3. Auto cleaning
            cleaned_df, cleaned_path = auto_clean_file(str(raw_path))

        st.success("Pipeline finished successfully ✅")

        # ---- SHOW RESULTS ----
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Schema Report")
            st.dataframe(schema_df)

        with col2:
            st.subheader("Rule Suggestions")
            for msg in suggestions:
                st.write("- " + msg)

        st.subheader("Cleaned Data (first 20 rows)")
        st.dataframe(cleaned_df.head(20))

        # ---- DOWNLOAD BUTTON ----
        st.download_button(
            label="📥 Download Cleaned CSV",
            data=cleaned_df.to_csv(index=False).encode("utf-8"),
            file_name="cleaned_data.csv",
            mime="text/csv",
        )

        st.markdown("---")
        st.markdown("**Saved files on disk:**")
        st.text(f"Schema report : {schema_path}")
        st.text(f"Suggestions   : {suggestions_path}")
        st.text(f"Cleaned CSV   : {cleaned_path}")
else:
    st.info("Upload a CSV file to start.")
