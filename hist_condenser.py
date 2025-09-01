# import sys
# import pandas as pd
# sys.path.insert(1,r'C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\Scripts\remodeled_design')
# from nanopore_sub_node_design import ReadData
# def summing_counts(data):
#     counter = 0
#     for elements in data['counts']:
#         if pd.notna(elements):
#             counter += int(elements)
#     return counter
# 
# file = r'C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\pacbio_histrogram\Nodehist_A22_TGG_vs_A23_TGG.csv'
# reader =  ReadData(file)
# data = reader.read_data()
# combination = set(data['Combination'])
# new_file = dict.fromkeys(combination,summing_counts(data))

import os
import sys
import pandas as pd

# Add module path for importing ReadData
sys.path.insert(1, r'C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\Scripts\remodeled_design')
from nanopore_sub_node_design import ReadData

# Input and output paths
input_folder = r'C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\pacbio_histrogram'
output_file = r'C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\Scripts\hist\aggregated_pacbio_counts.csv'

# Function to sum counts for a filtered dataframe
def summing_counts(data):
    counter = 0
    for elements in data['counts']:
        if pd.notna(elements):
            counter += int(elements)
    return counter

# Collect results in a list
results = []

# Loop through each file in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):
        filepath = os.path.join(input_folder, filename)
        reader = ReadData(filepath)
        data = reader.read_data()

        if 'Combination' not in data.columns or 'counts' not in data.columns:
            print(f'Combination column not in this file {filename}')  # Skip files missing required columns

        combinations = set(data['Combination'])
        count_sum = dict.fromkeys(combinations,summing_counts(data))
        value = list(count_sum.values())[0]
        for comb in combinations:
            if pd.isna(comb) or str(comb).strip() == '':
                continue
            else:
                results.append({
                    'filename': filename,
                    'combination': comb,
                    'total_count': value
                })

# Convert to DataFrame and save
results_df = pd.DataFrame(results)
results_df.to_csv(output_file, index=False)
print(f"Aggregated data saved to: {output_file}")
