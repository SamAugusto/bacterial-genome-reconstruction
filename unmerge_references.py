from Bio import SeqIO

for references in SeqIO.parse(
    r"C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\aligment_data\merged_24_references.fasta",
    "fasta",
):
    with open(
        rf"C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\aligment_data\{references.id}.fasta",
        "w",
    ) as file:
        file.write(f">{references.id}\n{str(references.seq)}\n")
    print(f"File {references.id} created")
