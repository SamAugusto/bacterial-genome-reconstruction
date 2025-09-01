from Bio import SeqIO

input_file = r"C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\aligment_data\Seaview\Seaview-Aligment_Results_Node_A2_TGG_vs_A3_AGG"
output_file = r"C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\aligment_data\Seaview\\240bp_double_sided_trim_A2_A3_trimmed.fasta"
trim = 240
with open(output_file,"w") as out_handle:
    for record in SeqIO.parse(input_file,'fasta'):
        record.seq = record.seq[trim:-trim]
        SeqIO.write(record, out_handle, "fasta")