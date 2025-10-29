import pandas as pd

df = pd.read_csv('data_collected/Data Engineer/profiles.csv', encoding='utf-8-sig')
print(f'Total profiles: {len(df)}')
print(f'Unique URLs: {df["URL"].nunique()}')
print(f'\nFirst few profiles:')
print(df[['Name', 'Title', 'Location']].head(10).to_string())

