import os
import pandas as pd

csv_path = "data_collected/Data Engineer/profiles.csv"

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    print(f"✅ Current profiles in file: {len(df)}")
    print(f"📊 Breakdown by location:")
    print(df['Location'].value_counts().head(10))
else:
    print("❌ CSV file not found")

