import os
import pandas as pd

def normalize_probe_pair(name):
    # Split by '_vs_' to isolate both probe names
    parts = name.split('_vs_')
    if len(parts) != 2:
        return name  # skip if not standard format

    # For each probe, remove suffix after the last underscore
    probe1 = '_'.join(parts[0].split('_')[:2])  # e.g., 'Probe_7'
    probe2 = '_'.join(parts[1].split('_')[:2])  # e.g., 'Probe_83'
    
    return f"{probe1}_vs_{probe2}"

# Apply normalization


folder = r'C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\seqkit_output_pacbio'
unique_m_values = set()

for root, dirs, files in os.walk(folder):
    for filename in files:
        if filename.endswith('_updated.csv'):
            file_path = os.path.join(root, filename)
            try:
                df = pd.read_csv(file_path)

                if df.shape[1] >= 1:
                    values = df.iloc[:, -1].dropna().unique()  # Last column
                    unique_m_values.update(values)
                    print(f" Processed: {filename} — Added {len(values)} new items")
                else:
                    print(f"️ {filename} has no columns")

            except Exception as e:
                print(f" Error reading {file_path}: {e}")

# Display summary
print(f"\n Total unique values from column M: {len(unique_m_values)}")
print(sorted(unique_m_values)[:10], '...')

cleaned_values = {item.split('-')[0] for item in unique_m_values if isinstance(item, str)}
nodes_500 = pd.read_excel(r'C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\BlatsnSummary_node_summary_node22.xlsx')
nodes_500_set = set(nodes_500.iloc[:,0])
nodes_500_set = {item.split('-')[0] for item in unique_m_values if isinstance(item, str)}
normalized_nodes_500_set = {normalize_probe_pair(name) for name in nodes_500_set}
nanopore_unique_nodes = {}
nanopore_unique_nodes['nodes'] = []
for elements in cleaned_values:
    if elements in normalized_nodes_500_set:
        nanopore_unique_nodes['nodes'].append(elements)
nanopore_unique_nodes['nodes'] = sorted(nanopore_unique_nodes['nodes'])
# Convert to DataFrame
df = pd.DataFrame(nanopore_unique_nodes['nodes'], columns=['nodes'])

# Save to Excel
output_path = r'C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\unique_nanopore_nodes.xlsx'
df.to_excel(output_path, index=False)

print(f"File saved to:\n{output_path}")

# Save all cleaned probe pairs (pre-normalization) into a separate Excel file
cleaned_values_df = pd.DataFrame(sorted(unique_m_values), columns=["cleaned_probes"])

combined_output_path = r'C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\combined_pacbio_nodes.xlsx'
cleaned_values_df.to_excel(combined_output_path, index=False)

print(f"Cleaned probes saved to:\n{combined_output_path}")
