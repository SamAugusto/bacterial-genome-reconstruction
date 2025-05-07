#This program was designed to sort only the node combinations in the remodeled_excel file
#since 2_90 = 90_2 I thought it would be easier to just create a separate module that does
#the operation of removing such duplicates without adding more complexity to the
#sub_node_design module
import pandas as pd

def combinations (unique_nodes):
    temp_lst = [node.split('_') for node in unique_nodes]
    seen = set()
    lst = []
    for pair in temp_lst:
        key = tuple(sorted(pair))
        if key not in seen:
            seen.add(key)
            lst.append(pair)
    rejoined = ['_'.join(pair) for pair in lst]
    return rejoined

if __name__ == '__main__':
    filepath = r'C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\pacbio_remodeled_data_design.xlsx'
    unique_nodes = pd.read_excel(filepath,sheet_name = 1)
    new_unique_nodes = combinations(unique_nodes['unique_nodes'])
    unique_df_cleaned = pd.DataFrame({'unique_nodes': new_unique_nodes})
    with pd.ExcelWriter(filepath, mode='a', if_sheet_exists='replace') as writer:
        unique_df_cleaned.to_excel(writer, sheet_name='Unique Nodes', index=False)    
    
    