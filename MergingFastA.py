import os

input_folder = r'C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\aligment_data\Fasta'
output_file = r'/aligment_data/merged_sequences.fasta'

with open(output_file, 'w') as merged_out:
    for filename in os.listdir(input_folder):
        if filename.endswith('.fasta') or filename.endswith('.fa'):
            file_path = os.path.join(input_folder, filename)
            with open(file_path, 'r') as infile:
                for line in infile:
                    merged_out.write(line)
                # Optional: add a newline between sequences
                merged_out.write('\n')

print(f" Merged raw FASTA saved to: {output_file}")
