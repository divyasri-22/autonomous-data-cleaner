import streamlit as st
import pandas as pd

st.title("Autonomous Data Cleaner")

uploaded = st.file_uploader("Upload a CSV file", type="csv")

if uploaded:
    df = pd.read_csv(uploaded)
    st.subheader("Raw Data")
    st.dataframe(df)

    # Simple cleaning
    df_clean = df.drop_duplicates().dropna(how="all")
    df_clean.columns = [c.strip().lower().replace(" ", "_") for c in df_clean.columns]

    st.subheader("Cleaned Data")
    st.dataframe(df_clean)

    st.download_button(
        "Download Cleaned CSV",
        df_clean.to_csv(index=False).encode("utf-8"),
        "cleaned.csv",
        "text/csv",
    )
