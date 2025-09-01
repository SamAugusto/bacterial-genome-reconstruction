import pandas as pd


def read_data(file: str, sheet_name: str = None) -> pd.DataFrame:
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


def append_columns_to_sheet(
    graph_path: str,
    sheet_name: str,
    cols,
    prefix: str = "checked_",
):
    # Load the sheet
    df = pd.read_excel(graph_path, sheet_name=sheet_name)

    # Normalize to a DataFrame
    if isinstance(cols, pd.Series):
        name = cols.name if cols.name is not None else "col"
        cols = cols.to_frame(name=name)

    # Rename output columns with a prefix to avoid collisions
    cols = cols.rename(columns=lambda c: f"{prefix}{c}")

    # Align lengths and fill with blanks
    cols = cols.reindex(range(len(df))).fillna("")

    # Append columns
    for c in cols.columns:
        df[c] = cols[c].values

    # Overwrite only that sheet
    with pd.ExcelWriter(graph_path, mode="a", if_sheet_exists="replace") as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(
        f"Appended {list(cols.columns)} to {graph_path} [{sheet_name}] with blanks filled"
    )


def check_nodes(graph_data: pd.DataFrame, design_data: pd.DataFrame) -> pd.DataFrame:
    sorted_design_nodes: set = set()
    sorted_nodes: list = []
    nodes_to_be_graphed: list = []
    for design_node in design_data["all_nodes"]:
        if pd.isna(design_node):
            continue
        splited_design_node = design_node.split("_")
        sorted_design_node: str = "_".join(sorted(splited_design_node))
        sorted_design_nodes.add(sorted_design_node)

    for node1, node2 in zip(graph_data["Node1"], graph_data["Node2"]):
        sorted_node: tuple = (
            "_".join(sorted(node1.split("_"))),
            "_".join(sorted(node2.split("_"))),
        )
        sorted_nodes.append(sorted_node)
    for nodes1, nodes2 in sorted_nodes:
        if nodes1 in sorted_design_nodes and nodes2 in sorted_design_nodes:
            nodes_to_be_graphed.append((nodes1, nodes2))
    return (
        pd.DataFrame(nodes_to_be_graphed, columns=["Node1", "Node2"])
        .drop_duplicates()
        .reset_index(drop=True)
    )


def checked_linkages(
    graph_data: pd.DataFrame, design_data: pd.DataFrame
) -> pd.DataFrame:
    sorted_linkages: list = []

    design_data_set = {
        "-".join(
            sorted(
                [
                    "_".join(sorted(sub_node1.strip().split("_"))),
                    "_".join(sorted(sub_node2.strip().split("_"))),
                ]
            )
        )
        for sub_node1, sub_node2 in design_data["linkage"]
        .dropna()
        .astype(str)
        .str.split("-", n=1)
    }

    for node1, node2 in zip(graph_data["Node1"], graph_data["Node2"]):
        sorted_nodes: str = "-".join(
            sorted(
                [
                    "_".join(sorted(str(node1).split("_"))),
                    "_".join(sorted(str(node2).split("_"))),
                ]
            )
        )
        if sorted_nodes in design_data_set:
            sorted_linkages.append(sorted_nodes)

    return (
        pd.DataFrame(sorted_linkages, columns=["checked_linkages"])
        .drop_duplicates()
        .reset_index(drop=True)
    )


def main():
    graph_path: str = (
        r"C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\Scripts\link\reduced_graph\linkage_Ends_withEXP_summary_AvgReadLenOver5kb_Aug17th.xlsx"
    )
    design_path: str = (
        r"C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\Scripts\link\reduced_graph\pacbio_node_linker_design_referencenew.xlsx"
    )

    graph_data: pd.DataFrame = read_data(
        graph_path, sheet_name="both node >=2 & filtering"
    )
    design_data: pd.DataFrame = read_data(design_path, sheet_name="11_Known_Strains")

    print(graph_data.head())
    print(design_data.head())
    checked_nodes: pd.DataFrame = check_nodes(graph_data, design_data)
    print(checked_nodes)

    append_columns_to_sheet(
        graph_path,
        sheet_name="both node >=2 & filtering",
        cols=checked_nodes[["Node1", "Node2"]],
        prefix="checked_",
    )
    checked_links: pd.DataFrame = checked_linkages(graph_data, design_data)
    append_columns_to_sheet(
        graph_path,
        sheet_name="both node >=2 & filtering",
        cols=checked_links,
        prefix="",  # no extra prefix, column is already "checked_linkages"
    )


if __name__ == "__main__":
    main()
