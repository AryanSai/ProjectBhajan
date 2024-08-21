import pandas as pd
from difflib import SequenceMatcher

def compute_similarity(original, predicted):
    similarity_score = SequenceMatcher(None, original, predicted).ratio()
    return similarity_score

df1 = pd.read_csv('Data/bhajans.csv')  
df2 = pd.read_csv('Data/Bajans_FullDetails.csv') 

df1['Bhajan'] = df1['Bhajan'].str.split('\n').str[0]

valid_rows = []

for _, row1 in df1.iterrows():
    for _, row2 in df2.iterrows():
        similarity = compute_similarity(row1['Bhajan'], row2['Title'])
        if similarity > 0.9:
            valid_rows.append({
                'Bhajan': row1['Bhajan'],
                'Deity': row1['Deity'],
                'Meaning': row1['Meaning'],
                'Level': row2['Level'],
                'Tempo': row2['Tempo'],
                'Language': row2['Language'],
                'Raga': row2['Raga']
            })

result_df = pd.DataFrame(valid_rows)

result_df.to_csv('merged_output.csv', index=False)
