import pandas as pd
from openpyxl import load_workbook

file_path = r'C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\kmer\sequences\10hits_pacbio_sequences.xlsx'
sourcelst = [
    '1_2', '2_3', '2_4',
    '3_3', '3_4', '3_5',
    '4_4', '4_5', '4_6',
    '5_4', '5_5', '5_6', '5_7',
    '6_6', '6_7', '6_8',
    '7_6', '7_7', '7_8', '7_9',
    '8_8', '8_9', '8_10',
    '9_9', '9_10', '9_11',
    '10_10', '10_11', '10_12',
    '11_10', '11_11',
    '12_11', '13_12'
]

def make_combination_key(sub_df):
    nodes = sub_df[['n1', 'n2']].values.tolist()
    normalized = sorted(set(tuple(sorted(pair)) for pair in nodes))  # 🔧 deduplicate and sort
    return "-".join(["_".join(pair) for pair in normalized])

for source_sheet in sourcelst:
    print(f"🔄 Processing sheet: {source_sheet}")
    
    df = pd.read_excel(file_path, sheet_name=source_sheet)
    df = df[df['hits'] > 10]
    if df.empty:
        print(f"⚠️ Skipping {source_sheet} — all hits ≤ 10")
        continue
    node_col = df.columns[4]
    nodes_probes_col = df.columns[5]

    #df[['n1', 'n2']] = df[node_col].str.extract(r'Probe_(\d+)_.*?_Probe_(\d+)_')
    #df[['n1', 'n2']] = df[node_col].str.extract(r'[A-Z](\d+)_.*?_vs_[A-Z](\d+)_')
    df[['n1', 'n2']] = df[node_col].str.extract(r'([A-Z]\d+)_\w+_vs_([A-Z]\d+)_\w+')

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

    print(f"✅ Finished: {source_sheet}")
