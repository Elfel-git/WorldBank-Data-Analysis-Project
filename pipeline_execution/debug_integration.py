"""
Debug script to check data_integration logic
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd() / 'modules'))

import pandas as pd
import numpy as np

# Load one CSV
csv_path = '../nam/GDP per capita (constant 2015 US$).csv'
df = pd.read_csv(csv_path, index_col=0)

print("=" * 60)
print("ORIGINAL CSV")
print("=" * 60)
print(f"Shape: {df.shape}")
print(f"Index (countries): {df.index[:3].tolist()}")
print(f"Columns (years): {df.columns[:3].tolist()}")
print(f"\nFirst 2 rows, first 3 cols:")
print(df.iloc[:2, :3])

print("\n" + "=" * 60)
print("AFTER STACK")
print("=" * 60)
stacked = df.stack()
print(f"Type: {type(stacked)}")
print(f"Index: {stacked.index[:3].tolist()}")
print(f"Values (sample): {stacked.iloc[:3].tolist()}")

print("\n" + "=" * 60)
print("AFTER RESET INDEX (long format)")
print("=" * 60)
long_df = stacked.reset_index()
long_df.columns = ['Country', 'Year', 'Value']
print(f"Shape: {long_df.shape}")
print(f"Columns: {long_df.columns.tolist()}")
print(f"Year values (sample): {long_df['Year'].unique()[:5].tolist()}")
print(f"Year dtype: {long_df['Year'].dtype}")

print("\n" + "=" * 60)
print("AFTER CLEANING YEAR (removing 'YR')")
print("=" * 60)
long_df['Year'] = long_df['Year'].astype(str).str.replace('YR', '').str.strip()
long_df['Year'] = pd.to_numeric(long_df['Year'], errors='coerce')
long_df['Indicator'] = 'GDP per capita (constant 2015 US$)'  # Add indicator name
print(f"Year values (sample): {long_df['Year'].unique()[:5].tolist()}")
print(f"Year dtype: {long_df['Year'].dtype}")
print(f"NaN years: {long_df['Year'].isna().sum()}")

print("\n" + "=" * 60)
print("SAMPLE DATA")
print("=" * 60)
print(long_df.head(10))

print("\n" + "=" * 60)
print("PIVOT TABLE TEST")
print("=" * 60)
pivoted = long_df.pivot(
    index=['Country', 'Year'],
    columns='Indicator',
    values='Value'
)
print(f"Pivoted shape: {pivoted.shape}")
print(f"Pivoted index: {pivoted.index[:3].tolist()}")
print(f"Pivoted columns: {pivoted.columns.tolist()}")

print("\n" + "=" * 60)
print("AFTER RESET INDEX (final format)")
print("=" * 60)
final = pivoted.reset_index()
print(f"Final shape: {final.shape}")
print(f"Final columns: {final.columns.tolist()}")
print(f"First 3 rows:")
print(final.head(3))
