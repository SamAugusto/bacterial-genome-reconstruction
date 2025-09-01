from linkage import read_data
import networkx as nx
import matplotlib.pyplot as plt
from itertools import permutations, combinations, islice
from networkx.exception import NetworkXNoPath, NodeNotFound
from collections import defaultdict


def make_graph(node_data):
    seen = set()
    G = nx.Graph()
    for idx, node in enumerate(node_data["Node1"]):
        if type(node) != str or type(node_data["Node2"][idx]) != str:
            print(f"{node} or {node_data['Node2'][idx]}, idex {idx}is not a string.")
        if node in seen and node_data["Node2"][idx] in seen:
            G.add_edge(node, node_data["Node2"][idx])
        elif node in seen:
            seen.add(node_data["Node2"][idx])
            G.add_node(node_data["Node2"][idx])
            G.add_edge(node, node_data["Node2"][idx])
        elif node_data["Node2"][idx] in seen:
            seen.add(node)
            G.add_node(node)
            G.add_edge(node_data["Node2"][idx], node)
        else:
            seen.add(node)
            seen.add(node_data["Node2"][idx])
            G.add_node(node)
            G.add_node(node_data["Node2"][idx])
            G.add_edge(node, node_data["Node2"][idx])
    pos = nx.spring_layout(G)  # Change to circular_layout if needed

    plt.figure(figsize=(25, 25))  # Larger figure to fit more nodes
    nx.draw(
        G,
        pos,
        with_labels=True,
        font_size=6,
        node_size=250,
        node_color="skyblue",
        edge_color="gray",
        linewidths=0.5,
        width=0.5,
    )
    plt.show()

    return G


# Uncoment this for all nodes paths
def new_all_leaf_paths(G, file_path="A2_A3_allpaths_new_data.txt"):
    if "A2_A3" not in G:
        print("A2_A3 is not in the graph")
        return 0

    seen = set()
    leaf_nodes = [n for n in G.nodes if G.degree[n] == 1]
    count = 0
    with open(file_path, "a", encoding="utf-8") as f:
        for target in leaf_nodes:  # changed
            source = "A2_A3"  # changed
            if target == source:  # changed
                continue  # changed
            print(source, target)
            for path in nx.all_simple_paths(G, source=source, target=target):
                tp = tuple(path)
                if tp in seen:
                    print("Alert: Duplicate path found!!!!!!!!!")
                    count += 1
                    continue
                seen.add(tp)
                f.write(" → ".join(str(node) for node in path) + "\n\n")
                print(
                    f"Path from {source} to {target}: {' → '.join(str(node) for node in path)}"
                )

    return count


# debugging function
# def new_all_leaf_paths(G, file_path="A2_A3_to_F22_F23.txt", max_edges=300):
#    source = "A2_A3"
#    target = "F22_F23"
#
#    # 1. sanity checks
#    if source not in G or target not in G:
#        print(f"Missing node. In graph? A2_A3={source in G}, H18_H19={target in G}")
#        return 0
#
#    print(f"A2_A3 degree {G.degree[source]}, F22_F23 degree {G.degree[target]}")
#
#    # 2. quick reachability test
#    if not nx.has_path(G, source, target):
#        print(f"No path between {source} and {target}")
#        return 0
#
#    # 3. iterate and record
#    dup_count = 0
#    path_count = 0
#    seen = set()
#
#    with open(file_path, "a", encoding="utf-8") as f:
#        for path in nx.all_simple_paths(
#            G, source=source, target=target, cutoff=max_edges
#        ):
#            t = tuple(path)
#            if t in seen:
#                print("Alert duplicate path found")
#                dup_count += 1
#                continue
#            seen.add(t)
#            path_count += 1
#            line = " → ".join(str(node) for node in path)
#            f.write(line + "\n")
#            print(f"Path {path_count}: {line}")
#
#    if path_count == 0:
#        print(f"No path between {source} and {target} within cutoff {max_edges}")
#
#    return dup_count


## Ignore this
# def all_shortest_leaf_paths(G):
#    leaf_nodes = [node for node in G.nodes if G.degree[node] == 1]
#    all_paths = defaultdict(list)
#    for source, target in permutations(leaf_nodes, 2):
#        try:
#            path = nx.shortest_path(G, source=source, target=target, cutoff=264)
#            all_paths[source].append(path)
#        except nx.NetworkXNoPath:
#            continue
#    return all_paths


if __name__ == "__main__":
    # Change this file
    file = r"C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\Scripts\link\graph_data\linkage_Ends_withEXP_summary_AvgReadLenOver5kb_Aug17th.xlsx"
    # file = r"C:\Users\user\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\Scripts\link\graph_data\linkage_Ends_withEXP_summary_AvgReadLenOver5kb.xlsx"
    node_data = read_data(file, sheet_name="figue_path>=2_designed_check")
    G = make_graph(node_data)

    try:
        counter = new_all_leaf_paths(G)
        print(counter)

    except nx.NodeNotFound as e:
        print(f"Node error: {e}")
#   except Exception as e:
#      print(f"An unexpected error occurred: {e}")
