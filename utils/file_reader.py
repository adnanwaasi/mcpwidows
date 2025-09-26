import pandas as pd 
from pathlib import Path 
DATA_DIR=Path(__file__).resolve().parent.parent/"datAa"

def read_csv_summary(filename):
    file_path=DATA_DIR/filename
    df = pd.read_csv(file_path)
    return f"CSV file {filename} has {len(df)} rows and {len(df.columns)} columns"

def read_parquet_summary(filename):
    file_path=DATA_DIR/filename
    df = pd.read_csv(file_path)
    return f"parquet file {filename} has {len(df)} rows and {len(df.columns)} columns"
