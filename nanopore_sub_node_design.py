import pandas as pd
import os
class ReadData:
    '''Reads the data of a spreadsheet file that is either .csv or .xlsx format'''
    def __init__(self,file):
        self.file = file
    def read_data(self):
        try:
            read_data = pd.read_csv(self.file)
            self.data = read_data
        except Exception:
            read_data = pd.read_excel(self.file)
            self.data = read_data
        return read_data
    def __repr__(self):
        return f"The data:\n {self.data} has been read"
    
    
class ProcessData:
    def __init__(self,data):
        self.data =data
    def remodel_data(self):
        remodeled_data =[]
        for cell in self.data['node_pairs']:
            if pd.isna(cell):
                remodeled_data.append(pd.NA)
            else:
                split_data = cell.split('-')
                split_data = split_data[0].split('_')+split_data[1].split('_')
                temp_lst_node_pairs = [split_data[5:],split_data[1],split_data[4]]
                remodeled_data.append(''.join(temp_lst_node_pairs[0])+'_'+'_'.join(temp_lst_node_pairs[1:]))
        self.nodes = remodeled_data
        return remodeled_data
    def distance_transfer(self):
        distance = []
        for dist,node in zip(self.data['distance'], self.data['node_pairs']):
            if pd.isna(node):
                distance.append(pd.NA)
            else:
                distance.append(dist)
        self.distance = distance
        return distance
    def unique_nodes(self):
        unique_nodes_data = []
        for cell in self.data['node_pairs']:
            if pd.isna(cell):
                unique_nodes_data.append(pd.NA)
            else:
                split_data = cell.split('-')
                split_data = split_data[0].split('_')+split_data[1].split('_')
                temp_lst_node_pairs = [split_data[1],split_data[4]]
                unique_nodes_data.append('_'.join(temp_lst_node_pairs))
        unique_nodes_data = list(dict.fromkeys(unique_nodes_data).keys())
        self.unique_nodes_data =  unique_nodes_data
        return unique_nodes_data
# if __name__ == '__main__':              
#     file_link = 'C:\\Users\\Samuel\\OneDrive - Drexel University\\Dr. Xiao Scripts Coop 2025\\seqkit_output_nanopore\\seqkit_output\\Hflu_86_028NP\\Hflu_86_028NP_ctg1_pairs_updated.csv'
#     ##Read Data
#     reader = ReadData(file_link)
#     design_data = reader.read_data()
#     
#     ##Process Unique nodes in a different dataframe
#     processor = ProcessData(design_data)
#     unique_nodes_list = processor.unique_nodes()
#     unique_df = pd.DataFrame({'unique_nodes': unique_nodes_list})
#     
#     ##Process Data
#     design_data['node_pairs'] = processor.remodel_data()
#     design_data['node_distance'] = processor.distance_transfer()
#     
# 
#     
#     ##Save File
#     with pd.ExcelWriter('remodeled_data_design.xlsx') as writer:
#         design_data.to_excel(writer, sheet_name='Full Data', index=False)
#         unique_df.to_excel(writer, sheet_name='Unique Nodes', index=False)
    
if __name__ == '__main__':
    base_folder = r"C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\seqkit_output_pacbio"
    output_path = r"C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\pacbio_remodeled_data_design.xlsx"

    all_full_data = []
    all_unique_nodes = []

    for root, _, files in os.walk(base_folder):
        for file in files:
            if file.endswith('_updated.csv'):
                file_path = os.path.join(root, file)
                print(f"🔄 Processing: {file_path}")

                try:
                    reader = ReadData(file_path)
                    design_data = reader.read_data()

                    processor = ProcessData(design_data)

                    # ✅ Step 1: Process unique nodes before modifying data
                    unique_nodes = processor.unique_nodes()
                    all_unique_nodes.extend(unique_nodes)

                    # ✅ Step 2: Process main data
                    design_data['node_pairs'] = processor.remodel_data()
                    design_data['node_distance'] = processor.distance_transfer()
                    design_data['source_file'] = file

                    # ✅ Step 3: Append full processed data
                    all_full_data.append(design_data)

                except Exception as e:
                    print(f"❌ Failed to process {file_path}: {e}")

    # ✅ Merge all collected data
    final_full_data = pd.concat(all_full_data, ignore_index=True)
    final_unique_df = pd.DataFrame({'unique_nodes': list(dict.fromkeys(all_unique_nodes).keys())})

    # ✅ Write to a single Excel workbook with two sheets
    with pd.ExcelWriter(output_path) as writer:
        final_full_data.to_excel(writer, sheet_name='Full Data', index=False)
        final_unique_df.to_excel(writer, sheet_name='Unique Nodes', index=False)

    print(f"✅ All processed data saved to:\n{output_path}")




