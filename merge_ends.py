
from score_sequence import sequence_parser
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO


def save_dict_to_fasta(seq_dict, output_path):
    records = []
    for seq_id, sequence in seq_dict.items():
        record = SeqRecord(Seq(str(sequence)), id=seq_id, description="")
        records.append(record)

    with open(output_path, "w") as fasta_out:
        SeqIO.write(records, fasta_out, "fasta")

if __name__ == '__main__':
    file_lst = input('Insert both files separated by a comma: ').split(',')
    file = 0
    sequences = []
    for file in range(len(file_lst)):
        sequences.append(sequence_parser(file_lst[file]))
    merged_seq = {key: sequences[0].get(key, 0) + sequences[1].get(key, 0)
              for key in set(sequences[0]) | set(sequences[1])}

    save_dict_to_fasta(merged_seq,r'C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\aligment_data\Seaview\end_nodes\A4_A5\FASTA\A4_A5_merged_ends.fasta')
