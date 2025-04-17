# Augusto Souza Seq_output nanopore 
import pandas as pd
import os


def compute_distances(data):
    '''Computes the distance between sequences from when they start until the next sequence starts'''
    start = data["start"].astype(int).tolist()
    distance = [start[i + 1] - start[i] for i in range(len(start) - 1)]
    distance.append(0)
    return distance


def link_pairs_combinations(data):
    '''Zips node pairs based on strand alternation and distance, skipping first '+' or '-' in ++- or --+ runs.'''
    pair_names = data['patternName']
    strands = data['strand']
    distances = data['distance'].astype(float).tolist()

    first_pair = [pair_names[j] for j in range(len(distances)) if 0 < distances[j] <= 700]
    second_pair = [pair_names[k] for k in range(len(distances)) if distances[k] > 700 or distances[k] == 0]
    first_strands = [strands[j] for j in range(len(distances)) if 0 < distances[j] <= 700]
    second_strands = [strands[k] for k in range(len(distances)) if distances[k] > 700 or distances[k] == 0]

    combinations = []
    for i in range(min(len(first_pair), len(second_pair))):
        if i + 2 < len(first_strands):
            if (first_strands[i] == first_strands[i + 1] and
                first_strands[i + 1] != first_strands[i + 2]):
                print(f"⏩ Skipping first '{first_strands[i]}' in a run at index {i}: ({first_pair[i]})")
                continue

        if first_strands[i] == second_strands[i]:
            print(f"⚠️ Skipping invalid same-strand pair: ({first_pair[i]}, {second_pair[i]}) — both '{first_strands[i]}'")
            continue

        combinations.append((first_pair[i], second_pair[i]))

    return combinations


def adding_blanks_with_seqid(combo, data):
    '''Inserts link pair strings aligned with the DataFrame size (only one per pair row).'''
    seq_id = data['seqID'].iloc[0]
    combo_strings = [f"{a},{b}_{seq_id}" for a, b in combo]
    link_pairs_column = [""] * len(data)
    for i in range(len(combo_strings)):
        link_pairs_column[i * 2] = combo_strings[i]
    return link_pairs_column


def add_node_pairs_column_from_link_pairs(data):
    '''Generates node_pairs column by pairing the 2nd probe of one link_pair with the 1st probe of the next.'''
    node_pairs = [""] * len(data)
    seq_id = data['seqID'].iloc[0]

    valid_link_rows = [i for i, val in enumerate(data['link_pairs']) if isinstance(val, str) and ',' in val]

    for idx in range(len(valid_link_rows) - 1):
        curr_idx = valid_link_rows[idx]
        next_idx = valid_link_rows[idx + 1]

        curr_pair = data.loc[curr_idx, 'link_pairs']
        next_pair = data.loc[next_idx, 'link_pairs']

        try:
            probe2 = curr_pair.split(',')[1].rsplit('_', 1)[0].strip()
            probe3 = next_pair.split(',')[0].strip()

            insert_row = curr_idx + 1
            if insert_row < len(data):
                node_pairs[insert_row] = f"{probe2.lower()},{probe3.lower()}_{seq_id}"
        except Exception as e:
            print(f"⚠️ Could not parse link_pairs at rows {curr_idx} & {next_idx}: {e}")

    return node_pairs



# Main script execution
if __name__ == "__main__":
    base_folder = r"C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\seqkit_output_nanopore\seqkit_output"

    print(f"📂 Scanning all subfolders inside:\n{base_folder}")

    for root, dirs, files in os.walk(base_folder):
        print(f"\n📁 Folder: {root}")
        for file in files:
            print(f"   - Found file: {file}")
            if file.endswith(".csv"):
                filepath = os.path.join(root, file)
                print(f"\n🚀 Processing: {filepath}")

                try:
                    df = pd.read_csv(filepath)
                    df = df.sort_values(by="start").reset_index(drop=True)
                    df["distance"] = compute_distances(df)
                    combo = link_pairs_combinations(df)
                    df["link_pairs"] = adding_blanks_with_seqid(combo, df)
                    df["node_pairs"] = add_node_pairs_column_from_link_pairs(df)

                    filename_no_ext = os.path.splitext(file)[0]
                    output_filename = f"{filename_no_ext}_pairs_updated.csv"
                    output_path = os.path.join(root, output_filename)

                    df.to_csv(output_path, index=False)
                    print(f"✅ Saved to: {output_path}")

                except Exception as e:
                    print(f"❌ Failed to process {filepath}: {e}")

