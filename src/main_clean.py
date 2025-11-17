import sys
import pandas as pd

from schema_report import generate_schema_report
from rule_suggestions import generate_rule_suggestions
from auto_cleaner import auto_clean_file  # this is already working in your project


def main(input_csv_path: str):
    print(f"INPUT FILE: {input_csv_path}")

    # STEP 1 – Schema report
    schema_df, schema_path = generate_schema_report(input_csv_path)

    # STEP 2 – Load raw data
    df = pd.read_csv(input_csv_path)

    # STEP 3 – Rule suggestions
    suggestions, suggestions_path = generate_rule_suggestions(df, input_csv_path)

    # STEP 4 – Auto cleaning (uses your existing auto_cleaner.py)
    cleaned_df, cleaned_path = auto_clean_file(input_csv_path)

    print("\n=== PIPELINE SUMMARY ===")
    print(f"Schema report saved to   : {schema_path}")
    print(f"Rule suggestions saved to: {suggestions_path}")
    print(f"Cleaned file saved to    : {cleaned_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main_clean.py <path_to_csv>")
        raise SystemExit(1)

    csv_path = sys.argv[1]
    main(csv_path)
