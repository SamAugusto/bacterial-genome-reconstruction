#This module was written with the purpose of creating column "O" called all_nodes in the remodeled data for
#pacbio and nanopore, with the purpose was to remove the string and keep all the sorted nodes
#even the repeated ones
from sub_node_design import ReadData
import pandas as pd

def all_nodes(node_pairs):
    nodes = []
    for cell in data['node_pairs']:
        if pd.isna(cell):
            nodes.append(pd.NA)
        else:
            temp_lst = sorted(cell.split('_'),key = lambda x:(len(x),x))
            nodes.append(temp_lst[0]+'_'+temp_lst[1])
    return nodes
def save_to_excel_sheet(new_data: pd.DataFrame, file_path: str, sheet_name: str):
    """
    Overwrites a specific sheet in an existing Excel file with new data.
    """

    with pd.ExcelWriter(file_path, mode='a', if_sheet_exists='replace', engine='openpyxl') as writer:
        new_data.to_excel(writer, sheet_name=sheet_name, index=False)



file_path = r'C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\remodeled_data_design\pacbio_remodeled_data_design.xlsx'
reader = ReadData(file_path)
data = reader.read_data()
new_nodes = all_nodes(data)
data['all_nodes'] = new_nodes
save_to_excel_sheet(data,file_path,'Full Data')
