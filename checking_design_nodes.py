import pandas as pd

from linkage import read_data


def normalize_node_name(node):
    """Ensure multi-part nodes like A2_A3 and A3_A2 are represented the same way."""
    if isinstance(node, str) and "_" in node:
        parts = node.split("_")
        parts.sort()
        return "_".join(parts)
    return node


def trim_data(design, data):
    design_nodes = set(normalize_node_name(n) for n in design["all_nodes"].values)
    data = data.copy()
    data["Node1"] = data["Node1"].apply(normalize_node_name)
    data["Node2"] = data["Node2"].apply(normalize_node_name)

    mask = data["Node1"].isin(design_nodes) & data["Node2"].isin(design_nodes)
    return data[mask].reset_index(drop=True)


if __name__ == "__main__":
    file_path_design = r"C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\Scripts\link\graph_data\pacbio_node_linker_design_reference.xlsx"
    file_path_data = r"C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\Scripts\link\graph_data\linkage_Ends_withEXP_summary_AvgReadLenOver5kb_Aug17th.xlsx"
    design = read_data(file_path_design, sheet_name="Unique_Nodes")
    data = read_data(file_path_data, sheet_name="both node >=2 & filtering")
    new_data = trim_data(design, data)
    with pd.ExcelWriter(
        file_path_data, engine="openpyxl", mode="a", if_sheet_exists="replace"
    ) as writer:
        new_data.to_excel(
            writer, sheet_name="figue_path>=2_designed_check", index=False
        )
