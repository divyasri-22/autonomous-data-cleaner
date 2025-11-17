import pandas as pd
import numpy as np
from pathlib import Path
import os


# ============================================================
#   MAIN FUNCTION: CLEAN ANY DATAFRAME
# ============================================================
def auto_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # ------------------------------------------------------------
    # 1. CLEAN DEPARTMENT COLUMN (IF EXISTS)
    # ------------------------------------------------------------
    if "department" in df.columns:

        def clean_dept(val):
            if pd.isna(val):
                return None
            v = str(val).strip().lower()

            mapping = {
                "hr": "HR",
                "h.r": "HR",
                "human resource": "HR",
                "human resources": "HR",

                "it": "IT",
                "i.t": "IT",
                "it dept": "IT",
                "it department": "IT",

                "finance": "Finance",
                "fin": "Finance",
                "f inance": "Finance",
            }

            if v in mapping:
                return mapping[v]
            return v.title()

        df["department"] = df["department"].apply(clean_dept)

    # ------------------------------------------------------------
    # 2. CLEAN JOINING DATE (IF EXISTS)
    # ------------------------------------------------------------
    if "joining_date" in df.columns:
        parsed = pd.to_datetime(
            df["joining_date"],
            errors="coerce",
            dayfirst=True
        )
        df["joining_date"] = parsed
        df = df.dropna(subset=["joining_date"])

    # ------------------------------------------------------------
    # 3. SALARY CLEANING (IF EXISTS)
    # ------------------------------------------------------------
    if "salary" in df.columns:
        # Remove negative values
        df.loc[df["salary"] < 0, "salary"] = pd.NA

        # Cap outliers (99th percentile)
        q99 = df["salary"].quantile(0.99)
        df.loc[df["salary"] > q99, "salary"] = q99

    # ------------------------------------------------------------
    # 4. REMOVE MISSING NAME ROWS
    # ------------------------------------------------------------
    if "name" in df.columns:
        df = df.dropna(subset=["name"])

    # ------------------------------------------------------------
    # 5. REMOVE NEGATIVE VALUES FROM ALL NUMERIC COLUMNS
    # ------------------------------------------------------------
    for col in df.select_dtypes(include=["int64", "float64"]).columns:
        df = df[df[col] >= 0]

    df = df.reset_index(drop=True)
    return df


# ============================================================
#   FILE-BASED CLEANER: LOAD CSV → CLEAN → SAVE
# ============================================================
def auto_clean_file(input_csv_path: str):
    """Load a CSV → clean using auto_clean_dataframe → save next to original."""
    in_path = Path(input_csv_path)
    df = pd.read_csv(in_path)

    cleaned_df = auto_clean_dataframe(df)

    # employees_raw.csv → employees_cleaned.csv
    out_path = in_path.parent / f"{in_path.stem.replace('_raw', '')}_cleaned.csv"
    cleaned_df.to_csv(out_path, index=False)

    print(f"\nSaved CLEANED file to: {out_path}")
    return cleaned_df, out_path


# ============================================================
#   TESTING MODE (RUN DIRECTLY)
# ============================================================
if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parents[1]
    raw_file = base_dir / "data" / "employees_raw.csv"

    print(f"Reading: {raw_file}")
    df_raw = pd.read_csv(raw_file)

    print("\n=== BEFORE CLEANING ===")
    print(df_raw.head())
    print(df_raw.describe(include="all"))

    df_clean = auto_clean_dataframe(df_raw)

    print("\n=== AFTER CLEANING ===")
    print(df_clean.head())
    print(df_clean.describe(include="all"))

    save_path = base_dir / "data" / "employees_cleaned_from_auto_func.csv"
    df_clean.to_csv(save_path, index=False)

    print(f"\nSaved CLEANED file to: {save_path}")
