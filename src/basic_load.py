import pandas as pd
from pathlib import Path

# 1. Locate the data folder (one level above src, in "data")
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"

# 2. Load the employees file
file_path = DATA_DIR / "employees_raw.csv"
df = pd.read_csv(file_path)

# 3. Build a simple schema report
report = {
    "column": [],
    "dtype": [],
    "missing_pct": [],
    "n_unique": [],
}

for col in df.columns:
    report["column"].append(col)
    report["dtype"].append(str(df[col].dtype))
    report["missing_pct"].append(round(df[col].isna().mean() * 100, 2))
    report["n_unique"].append(df[col].nunique())

schema_df = pd.DataFrame(report)

print("\n=== SCHEMA REPORT ===")
print(schema_df)

# 4. Save report to CSV
output_path = DATA_DIR / "employees_schema_report.csv"
schema_df.to_csv(output_path, index=False)
print(f"\nSaved schema report to: {output_path}")
