import sys
from pathlib import Path
import pandas as pd


def generate_schema_report(input_csv_path: str, output_csv_path: str | None = None):
    """Create a simple schema report (dtypes, missing %, uniques) for a CSV."""
    input_path = Path(input_csv_path)
    df = pd.read_csv(input_path)

    report_df = pd.DataFrame({
        "column": df.columns,
        "dtype": df.dtypes.astype(str).values,
        "missing_pct": df.isna().mean().values * 100,
        "n_unique": df.nunique(dropna=True).values
    })

    # Save next to the input file, e.g. employees_raw.csv -> employees_schema_report.csv
    if output_csv_path is None:
        out_dir = input_path.parent
        base_name = input_path.stem.replace("_raw", "")
        output_path = out_dir / f"{base_name}_schema_report.csv"
    else:
        output_path = Path(output_csv_path)

    report_df.to_csv(output_path, index=False)

    print("\n=== SCHEMA REPORT ===")
    print(report_df)
    print(f"\nSaved schema report to: {output_path}")

    return report_df, output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python schema_report.py <path_to_csv>")
        raise SystemExit(1)

    csv_path = sys.argv[1]
    generate_schema_report(csv_path)
