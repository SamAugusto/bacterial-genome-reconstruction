# Imports
from Bio import SeqIO
import os

#Functions
def get_score(fastq_file,record_name_lst):
    scores = {}
    for record in SeqIO.parse(fastq_file,'fastq'):
        if record.id.split('/')[1] in record_name_lst:
            quality_string = "".join(chr(q + 33) for q in record.letter_annotations["phred_quality"])
            scores[record.id.split('/')[1]] = quality_string
    return scores            
    
def get_aligment_data(fasta_file):
    record_lst = []
    record_seq_data = {}
    for record in SeqIO.parse(fasta_file,'fasta'):
        if record.id.lower().startswith('consensus'):
            continue
        record_lst.append(record.id)
        record_seq_data[record.id] = record.seq
    return record_lst, record_seq_data


def adding_dashes(sequence,score):
    new_score = []
    i = 0
    j = 0
    for i in range(len(sequence)):
        if sequence[i] == '-':
            pass
        else:
            new_score.append(score[j])
            j +=1
        i +=1
    return ''.join(new_score)
            
def combine_data(sequences,scores):
    seq_and_scores = {}
    for seqid in sequences.keys():
        seq_and_scores[seqid]=[sequences[seqid],adding_dashes(sequences[seqid],scores[seqid])]
    return seq_and_scores



def write_gapped_fastq(data_dict, output_path):
    with open(output_path, "w") as f:
        for rec_id, (sequence, quality_str) in data_dict.items():
            f.write(f"@{rec_id}\n")
            f.write(f"{sequence}\n")
            f.write("+\n")
            f.write(f"{quality_str}\n")
            
            
def batch_convert_fasta_directory(fasta_dir, fastq_input_file, output_dir):
    for root, dirs, files in os.walk(fasta_dir):
        for file in files:
            fasta_file = os.path.join(root, file)
            base_name = os.path.basename(fasta_file)
            output_fastq = os.path.join(output_dir, base_name.replace('.fasta', '').replace('.fa', '') + '.fastq')

            print(f"Trying: {fasta_file}")

            try:
                # Try parsing — continue only if at least one sequence is found
                aligment_data = get_aligment_data(fasta_file)
                if not aligment_data[0]:  # No records found
                    print(f"✗ Skipped (no sequences): {fasta_file}")
                    continue

                record_lst = aligment_data[0]
                sequences = aligment_data[1]
                scores = get_score(fastq_input_file, record_lst)
                converted_file_data = combine_data(sequences, scores)
                write_gapped_fastq(converted_file_data, output_fastq)
                print(f"✓ Saved: {output_fastq}")

            except Exception as e:
                print(f"✗ Error processing {fasta_file}: {e}")
    
if __name__ == '__main__':
    #Files
    fasta_file = r'C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\aligment_data\Seaview\double_sided\Aligned\aligned_sub_clusters\FASTA\sub_cluster_159058134.fasta'
    fastq_file = r'C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\aligment_data\Fastq\Node_A2_TGG_vs_A3_AGG.fastq'
    output_fastq = r'C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\aligment_data\Seaview\double_sided\Aligned\aligned_sub_clusters\FASTQ' +'\\'+fasta_file.split('\\')[-1].replace('fasta','fastq')




    aligment_data = get_aligment_data(fasta_file)
    record_lst = aligment_data[0]
    sequences = aligment_data[1]
    scores = get_score(fastq_file,record_lst)
    converted_file_data = combine_data(sequences,scores)
    write_gapped_fastq(converted_file_data, output_fastq)
    fasta_dir = r'C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\aligment_data\Seaview\double_sided\Aligned\aligned_sub_clusters\FASTA'
    output_dir = r'C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\aligment_data\Seaview\double_sided\Aligned\aligned_sub_clusters\FASTQ'

    print("\nRunning batch conversion...")
    batch_convert_fasta_directory(fasta_dir, fastq_file, output_dir)