# Imports Standard
import re

# Third Party Imports
from collections import defaultdict

import pandas as pd


# Functions
def read_data(file, sheet_name=None):
    if file.endswith(".csv"):
        data = pd.read_csv(file)
    elif file.endswith((".xls", ".xlsx")):
        if sheet_name:
            data = pd.read_excel(file, sheet_name=sheet_name)
        else:
            data = pd.read_excel(file)
    else:
        raise ValueError("File format not available for reading.")
    return data


def linking_nodes(nodes, all_links):
    """
    #If a subnode is in any linker then a node is possible
    ##List all linkers that subnode is present
    ### is there a subnode that has the second part of the linkers that the subnode was found
    ####Link the nodes
    #####Repeat for the other pair
    """
    nodes_linked = defaultdict(set)
    for node in nodes:
        for sub_node in node.split("-"):
            linkers_present = {
                linker
                for linker in all_links
                if any(sub_node == part for part in linker.split("-"))
            }
            for verified_linker in linkers_present:
                sub_linker_left, sub_linker_right = verified_linker.split("-")
                other_part = (
                    sub_linker_right if sub_node == sub_linker_left else sub_linker_left
                )
                for target_node in nodes:
                    target_left, target_right = target_node.split("-")

                    if other_part == target_left or other_part == target_right:
                        current_pair_sorted = tuple(sorted([node, target_node]))
                        existing_sorted = {
                            tuple(sorted(pairs))
                            for pairs in nodes_linked[verified_linker]
                        }

                        if current_pair_sorted not in existing_sorted:
                            nodes_linked[verified_linker].add((node, target_node))

    print("Nodes Linked:", nodes_linked)
    return nodes_linked


# Defining Excel Data
class ExcelData:
    def __init__(self, data):
        self.data = data

    def linkage_finder(self):
        all_linkages = set()
        all_linkages_num = {}
        for idx, linkages in enumerate(self.data.iloc[:, 0]):
            link = linkages.split("|")
            for node in link:
                new_node = node.replace("_end", "")
                link[link.index(node)] = new_node
            if len(link) == 2:
                link = "-".join(link)
                if link not in all_linkages:
                    all_linkages.add(link)
                    linkage_num = self.data.iloc[idx, 1]
                    all_linkages_num[link] = linkage_num
        print("This is the linkers:", all_linkages)
        return all_linkages, all_linkages_num

    def node_finder(self):
        raw_node_data = set(
            re.sub(r"_.GG", "", "-".join(nodes.split("_vs_")))
            for nodes in self.data.iloc[:, 0]
        )
        print("This is the nodes: ", raw_node_data)
        return raw_node_data


# ============================
# Processing the Input Data
# ============================

if __name__ == "__main__":

    # Gathering and Cleaning input data from raw data
    linkage_data = read_data(
        r"C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\Scripts\link\link_data\linkage_kmers_ReadsOver0_tosent_top50percent_coverageredo_tosent 1.xlsx",
        "linkage_Ends_ReadsOver0",
    )
    nodes_data = read_data(
        r"C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\Scripts\link\link_data\Combined_Histogram_Design_capmarison_7_9_2025_ALL_Nodes_Exp.xlsx",
        "Unmatched_Histogram_Exp",
    )
    nodes_data = ExcelData(nodes_data)
    nodes = nodes_data.node_finder()
    all_links, all_links_score = ExcelData(linkage_data).linkage_finder()

    # Edge Case if a node and a linker are the same report it as Node is a linker (may report it in the future)
    node_linkers = set(node_linker for node_linker in nodes if node_linker in all_links)
    print("These are node linkers:", node_linkers)

    # Linking Nodes
    nodes_linked = linking_nodes(nodes, all_links)

    # Finding Left Over Nodes and linkers
    leftover_nodes = nodes - set().union(*nodes_linked.values())
    leftover_linkers = all_links - nodes_linked.keys()

    # Assemblying Data Frame
    final_df = pd.DataFrame(
        [
            (linker, node1, node2)
            for linker, pairs in nodes_linked.items()
            for node1, node2 in pairs
        ],
        columns=["linker", "node_1", "node_2"],
    )
    df_leftover_nodes = list(leftover_nodes)
    df_leftover_linkers = list(leftover_linkers)

    diff_linkers = len(final_df) - len(df_leftover_linkers)
    if diff_linkers > 0:
        df_leftover_linkers.extend([None] * diff_linkers)
    final_df["left_over_linkers"] = df_leftover_linkers

    diff_nodes = len(final_df) - len(df_leftover_nodes)
    if diff_nodes > 0:
        df_leftover_nodes.extend([None] * diff_nodes)

    final_df["left_over_nodes"] = df_leftover_nodes

    final_df["linker#"] = final_df["linker"].map(all_links_score)

    # Saving DataFrame into Excel
    final_df.to_excel(
        r"C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\Scripts\link\link_data\linked_nodes.xlsx",
        index=False,
    )
    print("left_over_nodes:", leftover_nodes)
