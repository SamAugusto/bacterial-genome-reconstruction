##Augusto Souza Nodes organizing program

import re
import pandas as pd

df = pd.read_excel('filterd_kmersRaw_Mar27th_2025.xlsx', sheet_name=0, header=0)
df = df.dropna(how='all')
column_names = df.columns.tolist()
matrix = df.values.tolist()

def checkMatchingSequences(matrix):
    result = []
    for n in range(len(matrix)):
        if matrix[n][1] == 1 or matrix[n-1][1] == 1:
            result.append(matrix[n][4])
            if matrix[n][0] != matrix[n+1][0] if n+1 < len(matrix) else True:
                result.append(",")
    return result

def checkEnds(matrix):
    result = []
    for n in range(len(matrix)):
        if matrix[n][1] == 1 or matrix[n-1][1] == 1:
            result.append(matrix[n][6])
            if matrix[n][0] != matrix[n+1][0] if n+1 < len(matrix) else True:
                result.append(",")
    return result

def splittingSequences(sequences):
    grouped = []
    current_group = []
    for item in sequences:
        if item == ",":
            if current_group:
                grouped.append(current_group)
                current_group = []
        else:
            current_group.append(item)
    if current_group:
        grouped.append(current_group)
    return grouped

def splittingEnds(ends):
    grouped = []
    current_group = []
    for item in ends:
        if item == ",":
            if current_group:
                grouped.append(current_group)
                current_group = []
        else:
            current_group.append(item)
    if current_group:
        grouped.append(current_group)
    return grouped

def nodeProbecalculator(flst):
    result = []
    for group in flst:
        unique_pairs = set()
        unique_probes = set()
        for comparison in group:
            matches = re.findall(r'Probe_(\d+)_', comparison)
            if len(matches) == 2:
                pair = tuple(sorted(matches))
                unique_pairs.add(pair)
                unique_probes.update(pair)
        num_nodes = len(unique_pairs)
        num_problems = len(unique_probes)
        result.append((num_nodes, num_problems))
    return result

def countUniqueEnds(ends):
    counts = []
    for group in ends:
        unique_ends = set(group)
        counts.append(len(unique_ends))
    return counts

if __name__ == '__main__':
    out = checkMatchingSequences(matrix)
    flst = splittingSequences(out)
    rawend = checkEnds(matrix)
    ends = splittingEnds(rawend)

    node_probe_data = nodeProbecalculator(flst)
    end_counts = countUniqueEnds(ends)

    matched_indices = [i for i in range(len(matrix)) if matrix[i][1] == 1 or matrix[i-1][1] == 1]

    sequence_to_metrics = {}
    start_idx = 0
    for idx, group in enumerate(flst):
        sequence = matrix[matched_indices[start_idx]][0]
        sequence_to_metrics[sequence] = {
            "nodes": node_probe_data[idx][0],
            "probes": node_probe_data[idx][1],
            "ends": end_counts[idx]
        }
        start_idx += len(group)

    final_matrix = []
    for row in matrix:
        seq = row[0]
        if seq in sequence_to_metrics:
            metrics = sequence_to_metrics[seq]
            row[5] = f"{metrics['nodes']}:{metrics['probes']}"
            row[7] = str(metrics['ends'])
            final_matrix.append(row)

    df_out = pd.DataFrame(final_matrix, columns=column_names)
    df_out.to_excel("sequences.xlsx", index=False, header=True)
