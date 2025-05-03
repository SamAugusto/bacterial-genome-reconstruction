import pandas as pd
import itertools
def filters(file):
    try:
        node_500_nanopore = pd.read_csv(file)
    except Exception:
        node_500_nanopore = pd.read_excel(file)
    node_500_nanopore.rename(columns = {node_500_nanopore.columns[0]: 'nodes'}, inplace = True)
    #filtered_500 = [data for data in node_500_nanopore.iloc[:,0].drop_duplicates().reset_index(drop=True) if data.startswith('Probe')] nanopore
    filtered_500 = [
        data for data in node_500_nanopore.iloc[:, 0].drop_duplicates().reset_index(drop=True)
        if data and data[0].isupper()
    ]#pacbio
    return filtered_500
def intersection(ven,dia):#Check for reverse order as well
    data_intersection = []
    ven = set(ven)
    for elements in dia:
        if elements in ven:
            data_intersection.append(elements)
    return data_intersection
def subtract(list1,list2):
    '''unique_nodes_in_the_nanopore_design_but_not_in_the_experimental_nodes
   or unique_nodes_in_the_experimental_nodes_but_not_in_the_nanopore_design'''
    return list(set(list1)-set(list2))
def array_fixer(list_of_arrays):
    bigg_array = max(len(arrays) for arrays in list_of_arrays)
    fixed_arrays = []
    for columns in list_of_arrays:
        if len(columns) < bigg_array:
            columns += [''] * (bigg_array - len(columns))
            # if arrays are not in the same size as the larger array:
            # fill in blanks until they are:
            fixed_arrays.append(columns)
        else:
            fixed_arrays.append(columns)
    # return a list of full sized arrays
    return fixed_arrays
def normalize_data1(data_1):
    temp_data = [data.split('_Vs_') for data in data_1]
    data_1 = [ '_vs_'.join(normalized) for normalized in temp_data]
    return data_1
def sorting_data(data):# still wrong fix it later
    temp_data = [i.split('_vs_') for i in data]
    sorted_data = [sorted(pair) for pair in temp_data]
    data = [ '_vs_'.join(normalized) for normalized in sorted_data]
    return data
class Data:
    def __init__(self,node_lst):
        self.node_list = node_lst
    
    def combinations (self):
        temp_lst = [x.split('_vs_') for x in self.node_list]
        seen = set()
        lst = []
        for pair in temp_lst:
            key = tuple(sorted(pair))
            if key not in seen:
                seen.add(key)
                lst.append(pair)
        rejoined = ['_vs_'.join(pair) for pair in lst]
        return rejoined
    def list_to_array(self):
        final_df = pd.DataFrame({
            'Experimental Design': self.node_list[0],
            'Theoretical Design': self.node_list[1],
            'Intersection Between Experimental data and Theoretical Design': self.node_list[2],
            'unique_nodes_in_the_nanopore_design_but_not_in_the_experimental_nodes': self.node_list[3],
            'unique_nodes_in_the_experimental_nodes_but_not_in_the_nanopore_design': self.node_list[4]
        })
        return final_df

        
if __name__ == '__main__':
    #exp_data = input("Enter path to experimental CSV/XLSX file: ")
    #design_data = input("Enter path to theoretical design file")
    #File for Desktop
    #exp_data = r'C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\BlatsnSummary_node_summary_500nodeOver5reads.csv'
    #File for Laptop
    exp_data = r'C:\Users\user\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\BlatsnSummary_node_summary_node22.xlsx'


    data_0 = filters(exp_data) #first column of concat file 500 node
    #File for Desktop
    #design_data = r'C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\node_comparisson\nanopore_unique_nodes.xlsx'
    #File for laptop
    design_data = r'C:\Users\user\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\node_comparisson\pacbio_unique_nodes.xlsx'

    data_1= filters(design_data)# 2nd column theoretical design
    #data_1 = normalize_data1(data_1) only for nanopore
    data_1 = sorting_data(data_1)
    data_0 = sorting_data(data_0)
    
    data_2 =intersection(data_0,data_1) # 3rd intersection
    data_3 = subtract(data_1 , data_0) #unique_nodes_in_the_nanopore_design_but_not_in_the_experimental_nodes
    data_4 = subtract(data_0 , data_1)# unique_nodes_in_the_experimental_nodes_but_not_in_the_nanopore_design

    data_cols = [
        Data(data_0).combinations(),
        Data(data_1).combinations(),
        Data(data_2).combinations(),
        Data(data_3).combinations(),
        Data(data_4).combinations()
    ]

    data_cols_fixed = array_fixer(data_cols)
    final_df = Data(data_cols_fixed).list_to_array()
    #Desktop File
    #final_df.to_excel(r"C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\nodes_comparisson.xlsx", index =False)
    #Laptop File
    final_df.to_excel(r"C:\Users\user\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\pacbio_nodes_comparisson.xlsx", index =False)