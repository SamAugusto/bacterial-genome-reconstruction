import os
import pandas as pd
#Augusto Souza Seq_output nanopore

def compute_distances(data):
    start = data["start"].astype(int).tolist()
    distance = [start[i+1] -start[i] for i in range(len(start)-1)]
    distance.append(0)
    return distance
def node_pairs_combinations(data):
    pair_names = data['patternName']
    strands = data['strand']
    distances = data['distance'].astype(float).tolist()
    i = 0
    first_pair = []
    second_pair = []
    first_strands = []
    second_strands = []
    index = []
    while i < len(strands) - 1:
        if strands[i] == '+' and strands [i+1] =='-' :
#        if (
#                strands[i] == '+' and
#                strands[i + 1] == '-' and
#                (
#                        (i + 3 < len(strands) and strands[i + 2] == '+' and strands[i + 3] == '-') or
#                        (i + 2 >= len(strands))  # allow final + - pair at end of list
#                )
#        ):
            print(f"Pairing index {i}: {strands[i]} -> {strands[i+1]}")
            first_strands.append('+')
            second_strands.append('-')
            if (0 < distances[i] <= 700) and (distances[i+1] > 700 or distances[i+1] == 0):
                first_pair.append(pair_names[i])
                second_pair.append(pair_names[i+1])
                index.append(i)
            i += 2
        else:
            i += 1
    combinations= zip(zip(first_pair,second_pair), index)
    return [(a,b,c) for (b,c),a in combinations]
def adding_blanks(combo, data):
    node_pairs_column = [""] * len(data)
    for idx, first, second in combo:
        node_pairs_column[idx] = f"{first},{second}" 
    return node_pairs_column
def add_node_pairs_column_from_link_pairs(data):
    '''Generates node_pairs column as: Probe_2_vs_Probe_90-Hflu_86_028NP_ctg1'''
    node_pairs = [""] * len(data)
    seq_id = data['seqID'].iloc[0]

    valid_link_rows = [i for i, val in enumerate(data['link_pairs']) if isinstance(val, str) and ',' in val]

    for idx in range(len(valid_link_rows) - 1):
        curr_idx = valid_link_rows[idx]
        next_idx = valid_link_rows[idx + 1]
        if next_idx-curr_idx == 2:
            curr_pair = data.loc[curr_idx, 'link_pairs']
            next_pair = data.loc[next_idx, 'link_pairs']

            try:
                probe2 = "_".join(curr_pair.split(',')[1].split('_')[:2]).strip()  # gets 'Probe_2'
                probe3 = next_pair.split(',')[0].strip()                           # gets 'Probe_90'

                insert_row = curr_idx + 1
                if insert_row < len(data):
                    node_pairs[insert_row] = f"{probe2}_vs_{probe3}-{seq_id}"
            except Exception as e:
                print(f"⚠️ Could not parse link_pairs at rows {curr_idx} & {next_idx}: {e}")

    return node_pairs





if __name__ == "__main__":
    base_folder = r"C:\Users\user\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\seqkit_output_human"

    print(f"📂 Scanning all subfolders inside:\n{base_folder}")

    for root, dirs, files in os.walk(base_folder):
        print(f"\n📁 Folder: {root}")
        for file in files:
            if file.endswith(".csv"):
                filepath = os.path.join(root, file)
                print(f"\n🚀 Processing: {filepath}")

                try:
                    df = pd.read_csv(filepath)
                    df = df.sort_values(by="start").reset_index(drop=True)
                    df["distance"] = compute_distances(df)
                    combo = node_pairs_combinations(df)
                    df["link_pairs"] = adding_blanks(combo, df)
                    df["node_pairs"] = add_node_pairs_column_from_link_pairs(df)
                    # Save with new filename
                    filename_no_ext = os.path.splitext(file)[0]
                    output_filename = f"{filename_no_ext}_pairs_updated.csv"
                    output_path = os.path.join(root, output_filename)

                    df.to_csv(output_path, index=False)
                    print(f"✅ Saved to: {output_path}")

                except Exception as e:
                    print(f"❌ Failed to process {filepath}:\n{e}")
