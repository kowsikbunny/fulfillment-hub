import pandas as pd
import os

print("FULFILLMENT HUB DATA CHECK")
print("=" * 60)

for file in os.listdir("data"):
    if file.endswith(".csv"):
        path = os.path.join("data", file)
        df = pd.read_csv(path)

        print(f"\n{file}")
        print(f"Rows: {len(df)}")
        print(f"Columns: {len(df.columns)}")
        print("Column names:")
        print(list(df.columns))
        print("-" * 60)