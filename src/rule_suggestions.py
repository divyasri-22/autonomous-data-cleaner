import pandas as pd
from pathlib import Path

def generate_rule_suggestions(df: pd.DataFrame, input_csv_path: str):
    """
    Analyse a DataFrame and generate human-readable cleaning suggestions.

    Returns
    -------
    messages : list[str]
        List of suggestion sentences.
    suggestions_path : str
        Path of the .txt file where suggestions were saved.
    """
    messages = []

    for col in df.columns:
        s = df[col]
        col_name = f"[{col}]"

        # Missing values
        missing_pct = s.isna().mean() * 100
        if missing_pct > 0:
            messages.append(
                f"{col_name} has {missing_pct:.1f}% missing -> suggest: impute or drop rows."
            )

        # Categorical / text-like
        if s.dtype == "object":
            non_null = s.dropna().astype(str)
            if not non_null.empty:
                unique_ratio = non_null.nunique() / len(non_null)
                if unique_ratio < 0.5:
                    messages.append(
                        f"{col_name} looks like a categorical column -> suggest: normalise case/typos."
                    )

            # Heuristic: column name hints date
            if "date" in col.lower():
                messages.append(
                    f"{col_name} may be a date stored as text -> suggest: parse to datetime and standardise format."
                )

        # Numeric checks
        if pd.api.types.is_numeric_dtype(s):
            if (s < 0).any():
                messages.append(
                    f"{col_name} has negative values -> suggest: disallow negatives or verify data source."
                )

            non_null_num = s.dropna()
            if not non_null_num.empty:
                q1 = non_null_num.quantile(0.25)
                q3 = non_null_num.quantile(0.75)
                iqr = q3 - q1
                upper = q3 + 3 * iqr
                if (non_null_num > upper).any():
                    messages.append(
                        f"{col_name} has possible high outliers -> suggest: cap or manually review extremes."
                    )

    # Save to .txt (UTF-8 so no Windows encoding drama)
    input_path = Path(input_csv_path)
    out_path = input_path.with_name(f"{input_path.stem}_rule_suggestions.txt")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("AUTO RULE SUGGESTIONS\n\n")
        for m in messages:
            f.write("- " + m + "\n")

    return messages, str(out_path)


# Allow running this file directly from terminal for testing
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python rule_suggestions.py path/to/file.csv")
        sys.exit(1)

    csv_path = sys.argv[1]
    df = pd.read_csv(csv_path)
    msgs, path = generate_rule_suggestions(df, csv_path)
    print("\n=== AUTO RULE SUGGESTIONS ===\n")
    for m in msgs:
        print("- " + m)
    print(f"\nSaved suggestions to: {path}")
