from difflib import SequenceMatcher
import pandas as pd

def compute_similarity(original, predicted):
    similarity_score = SequenceMatcher(None, original, predicted).ratio()
    return similarity_score

bajan= "Amba Bhavaani Shiva Shambhu Kumaara "
bajan2 = "Amba Bhavani Shiva Shambhu Kumara"
print(compute_similarity(bajan,bajan2))

df1 = pd.read_csv('Data/bhajans.csv')  
df2 = pd.read_csv('Data/Bajans_FullDetails.csv') 

df1['Bhajan'] = df1['Bhajan'].str.split('\n').str[0]

merged_df = pd.merge(df1, df2, how='inner', left_on=['Deity'], right_on=['Title'])

result_df = merged_df[['Bhajan', 'Deity', 'Meaning', 'Level', 'Tempo', 'Language', 'Raga']]

# Save the result to a new CSV file
result_df.to_csv('merged_output.csv', index=False)
