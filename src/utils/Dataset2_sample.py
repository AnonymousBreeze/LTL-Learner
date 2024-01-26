import pandas as pd

df = pd.read_csv('Dataset/NL_to_LTL_Synthetic_Dataset.csv')

sampled_df = pd.DataFrame(columns=['en', 'ltl'])
unique_pair_types = df['pair_type'].unique()
sample_size = 30

for pair_type in unique_pair_types:
    pair_type_df = df[df['pair_type'] == pair_type]
    if len(pair_type_df) >= sample_size:
        sampled_rows = pair_type_df.sample(n=sample_size, random_state=42)
    else:  
        sampled_rows = pair_type_df
    sampled_en_ltl = sampled_rows[['en', 'ltl']]
    sampled_df = pd.concat([sampled_df, sampled_en_ltl])

sampled_df.to_excel('Dataset/sampled_240_1.xlsx', index=False)
