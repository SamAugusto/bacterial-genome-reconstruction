import os
from Bio import SeqIO

input_folder = r'C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\aligment_data\Seaview\end_nodes\A4_A5\FASTQ'
output_folder = r'C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\aligment_data\Seaview\end_nodes\A4_A5\FASTA'

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Loop through each FASTQ file
for filename in os.listdir(input_folder):
    if filename.endswith('.fastq') or filename.endswith('.fq'):
        input_path = os.path.join(input_folder, filename)
        output_filename = os.path.splitext(filename)[0] + '.fasta'
        output_path = os.path.join(output_folder, output_filename)

        with open(output_path, 'w') as fasta_out:
            for record in SeqIO.parse(input_path, 'fastq'):
                parts = record.id.split('/')
                if len(parts) > 1:
                    record.id = parts[1]
                else:
                    record.id = parts[0]  # fallback in case '/' is missing
                record.name = record.id
                record.description = ''
                SeqIO.write(record, fasta_out, 'fasta')

        print(f"Converted {filename} to {output_filename} with updated IDs")

