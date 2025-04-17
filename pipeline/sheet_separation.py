import pandas as pd
from openpyxl import load_workbook

file_path = 'sequences.xlsx'
sourcelst = ['1_2','2_3','2_4',"3_4","3_5",'4_4','4_5','4_6','5_5','5_6','5_7','6_6','6_8']

def make_combination_key(sub_df):
    nodes = sub_df[['n1', 'n2']].values.tolist()
    normalized = sorted(set(tuple(sorted(pair)) for pair in nodes))
    return "-".join(["_".join(pair) for pair in normalized])

for source_sheet in sourcelst:
    print(f"Processing sheet: {source_sheet}")
    
    df = pd.read_excel(file_path, sheet_name=source_sheet)
    node_col = df.columns[4]
    nodes_probes_col = df.columns[5]

    df[['n1', 'n2']] = df[node_col].str.extract(r'Probe_(\d+)_.*?_Probe_(\d+)_')

    group_keys = []
    for seq in df['Kmer_seq'].unique():
        sub_df = df[df['Kmer_seq'] == seq]
        key = make_combination_key(sub_df)
        group_keys.extend([key] * len(sub_df))

    df['combo_key'] = group_keys
    df['probe_pair'] = df[nodes_probes_col].str.replace(':', '_', regex=False)
    df['sheet_name'] = df['probe_pair'] + '__' + df['combo_key']

    with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        for sheet_name, group_df in df.groupby('sheet_name'):
            safe_name = sheet_name[:31]
            group_df = group_df.drop(columns=['n1', 'n2', 'combo_key', 'probe_pair', 'sheet_name'])
            group_df.to_excel(writer, sheet_name=safe_name, index=False)

    print(f"Finished: {source_sheet}")
