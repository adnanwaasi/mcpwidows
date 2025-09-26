import pandas as pd
# Read the CSV
df = pd.read_csv("datAa/sample.csv")
# Save as Parquet
df.to_parquet("datAa/sample.parquet", index=False)
