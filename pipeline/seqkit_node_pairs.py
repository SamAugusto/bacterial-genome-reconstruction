# Augusto Souza Seq_output nanopore - CSV Fixed
import pandas as pd
import os


def compute_distances(data):
    '''Computes the distance between sequences from when they start untill the next sequence starts'''
    start = data["start"].astype(int).tolist()
    distance = [start[i + 1] - start[i] for i in range(len(start) - 1)]
    distance.append(0)
    return distance

def node_pairs_combinations(data):
    '''Using lists and tuples zips the node pairs based on the distance between sequences'''
    pair_names = data['patternName']
    strands = data['strand']
    distances = data['distance'].astype(float).tolist()

    first_pair = [pair_names[j] for j in range(len(distances)) if 0 < distances[j] <= 700]
    second_pair = [pair_names[k] for k in range(len(distances)) if distances[k] > 700 or distances[k] == 0]
    first_strands = [strands[j] for j in range(len(distances)) if 0 < distances[j] <= 700]
    second_strands = [strands[k] for k in range(len(distances)) if distances[k] > 700 or distances[k] == 0]

    combinations = []
    for i in range(min(len(first_pair), len(second_pair))):
        if first_strands[i] == second_strands[i]:
            print(f"⚠️ Skipping invalid same-strand pair: ({first_pair[i]}, {second_pair[i]}) — both '{first_strands[i]}'")
            continue
        combinations.append((first_pair[i], second_pair[i]))

    return combinations

def adding_blanks_with_seqid(combo, data):
    '''To output the data correctly we need to match the proper data size so adds blanks as
a place holder in the cells where there are empty pairs. In other words the pairs are being output in 1 cell but there are 2
input cells and if we merge the data it wont work because it does not match so we have to add blank spaces for the data'''
    seq_id = data['seqID'].iloc[0]
    combo_strings = [f"{a},{b}_{seq_id}" for a, b in combo] #additional requirement for organization
    node_pairs_column = [""] * len(data)
    for i in range(len(combo_strings)):
        node_pairs_column[i * 2] = combo_strings[i]
    return node_pairs_column

#main coding block runs in all the scripts from the data
if __name__ == "__main__":
    base_folder = r"C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\seqkit_output_nanopore\seqkit_output"

    print(f"📂 Scanning all subfolders inside:\n{base_folder}")

    for root, dirs, files in os.walk(base_folder):
        print(f"\n Folder: {root}")
        for file in files:
            print(f"   - Found file: {file}")
            if file.endswith(".csv"):
                filepath = os.path.join(root, file)
                print(f"\nProcessing: {filepath}")

                try:
                    df = pd.read_csv(filepath)
                    df = df.sort_values(by="start").reset_index(drop=True)
                    df["distance"] = compute_distances(df)
                    combo = node_pairs_combinations(df)
                    df["node_pairs"] = adding_blanks_with_seqid(combo, df)

                    filename_no_ext = os.path.splitext(file)[0]
                    output_filename = f"{filename_no_ext}_pairs_updated.csv"
                    output_path = os.path.join(root, output_filename)

                    df.to_csv(output_path, index=False)
                    print(f"Saved to: {output_path}")

                except Exception as e:
                    print(f"Failed to process {filepath}: {e}")
