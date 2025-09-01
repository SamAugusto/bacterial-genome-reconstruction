import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from remodeled_design.nanopore_sub_node_design import ReadData
if __name__ == '__main__':              
    file_link = r'C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\kmer\filterd_kmersRaw_ReadsOver_5_Coverage50%.csv'
    ##Read Data
    reader = ReadData(file_link)
    design_data = reader.read_data()
    design_data['Kmer_seq'] = design_data['Kmer_seq'].str.strip()
    design_data = design_data.sort_values(by='Kmer_seq', ignore_index=True)
    print(design_data)
    res = []
    for sequences in range(len(design_data['Kmer_seq'])-1):
        if design_data['Kmer_seq'][sequences] == design_data['Kmer_seq'][sequences+1]:
            res.append(1)
        else:
            res.append(0)
    res.append(0)
    design_data['I'] = res
    base, ext = os.path.splitext(file_link)
    new_file = f"{base}_V2{ext}"
    design_data.to_csv(new_file, index=False)

    print(f"Updated file saved as: {new_file}")   