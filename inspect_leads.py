import pandas as pd
import sys

try:
    file_path = "Leads March 2026.xlsx"
    df = pd.read_excel(file_path)
    print("Columns in the file:")
    print(df.columns.tolist())
    print("\nFirst few rows:")
    print(df.head())
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
