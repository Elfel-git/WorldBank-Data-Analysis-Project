from pathlib import Path
import pandas as pd
import re

BASE_DIR = Path(__file__).resolve().parent

INPUT_FILES = {
    "Edu_Spending_GDP_raw.csv": "Edu_Spending_GDP",
    "GDP_per_Capita_raw.csv": "GDP_per_Capita",
    "Health_Spending_GDP_raw.csv": "Health_Spending_GDP",
    "Internet_Usage_raw.csv": "Internet_Usage",
    "Learning_Outcome_raw.csv": "Learning_Outcome",
    "Unemployment_Rate_raw.csv": "Unemployment_Rate",
    "Population_Total_raw.csv": "Population_Total",
    "Inflation_Rate_raw.csv": "Inflation_Rate",
    "Trade_Openness_GDP_raw.csv": "Trade_Openness_GDP",
}

OUTPUT_FILE = BASE_DIR / "merged_raw_data.csv"


def to_long_format(df: pd.DataFrame, value_name: str) -> pd.DataFrame:
    year_columns = [col for col in df.columns if re.match(r"^YR\d{4}$", str(col))]
    long_df = df.melt(
        id_vars=["economy"],
        value_vars=year_columns,
        var_name="Year",
        value_name=value_name,
    )
    long_df["Year"] = long_df["Year"].str.replace("YR", "", regex=False).astype(int)
    return long_df


def main() -> None:
    merged_df = None

    for file_name, indicator_name in INPUT_FILES.items():
        file_path = BASE_DIR / file_name
        current_df = pd.read_csv(file_path)
        current_long = to_long_format(current_df, indicator_name)

        if merged_df is None:
            merged_df = current_long
        else:
            merged_df = merged_df.merge(current_long, on=["economy", "Year"], how="outer")

    merged_df = merged_df.sort_values(["economy", "Year"]).reset_index(drop=True)

    merged_df.to_csv(OUTPUT_FILE, index=False)
    print(f"Merged file saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
