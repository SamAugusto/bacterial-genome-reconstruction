import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from new_graph import read_data


def make_graph_separate_columns(node_data: pd.DataFrame):
    seen = set()
    G = nx.Graph()

    # iterate smartly over the two columns
    for n1, n2 in zip(node_data["checked_Node1"], node_data["checked_Node2"]):
        if not isinstance(n1, str) or not isinstance(n2, str):
            print(f"{n1} or {n2} is not a string.")
            continue

        if n1 in seen and n2 in seen:
            G.add_edge(n1, n2)
        elif n1 in seen:
            seen.add(n2)
            G.add_node(n2)
            G.add_edge(n1, n2)
        elif n2 in seen:
            seen.add(n1)
            G.add_node(n1)
            G.add_edge(n2, n1)
        else:
            seen.update([n1, n2])
            G.add_node(n1)
            G.add_node(n2)
            G.add_edge(n1, n2)

    # layout and plot
    pos = nx.spring_layout(G)  # or nx.circular_layout(G)
    plt.figure(figsize=(25, 25))
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


def make_single_col_graph(node_data: pd.DataFrame):
    seen = set()
    G = nx.Graph()

    # iterate smartly over the two columns
    for linkages in node_data["checked_linkages"]:
        if pd.isna(linkages):
            continue
        n1, n2 = linkages.split("-")
        if not isinstance(n1, str) or not isinstance(n2, str):
            print(f"{n1} or {n2} is not a string.")
            continue

        if n1 in seen and n2 in seen:
            G.add_edge(n1, n2)
        elif n1 in seen:
            seen.add(n2)
            G.add_node(n2)
            G.add_edge(n1, n2)
        elif n2 in seen:
            seen.add(n1)
            G.add_node(n1)
            G.add_edge(n2, n1)
        else:
            seen.update([n1, n2])
            G.add_node(n1)
            G.add_node(n2)
            G.add_edge(n1, n2)

    # layout and plot
    pos = nx.spring_layout(G)  # or nx.circular_layout(G)
    plt.figure(figsize=(25, 25))
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


def new_all_leaf_paths(G, file_path="A2_A3_all_paths_new_design_data.txt"):
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


def main():
    nodes_and_linkage_data = read_data(
        r"C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\Scripts\link\reduced_graph\linkage_Ends_withEXP_summary_AvgReadLenOver5kb_Aug17th.xlsx",
        sheet_name="both node >=2 & filtering",
    )
    separate_cols_graph = make_graph_separate_columns(nodes_and_linkage_data)
    single_col_graph = make_single_col_graph(nodes_and_linkage_data)
    new_all_leaf_paths(
        separate_cols_graph, "separate_column_A2_A3_all_paths_new_design_data.txt"
    )
    new_all_leaf_paths(
        single_col_graph, file_path="single_column_A2_A3_all_paths_new_design_data.txt"
    )


if __name__ == "__main__":
    main()
