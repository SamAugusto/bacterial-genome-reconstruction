from Bio import SeqIO
from Bio.SeqRecord import SeqRecord


def save_file(output_file,filtered_records):
    '''saves the fasta file'''
    with open(output_file, 'w') as out_handle:
        SeqIO.write(filtered_records, out_handle, 'fasta')
        
        
def filter_data(input_file,valid_seq):
    ''' Filter and store matching records'''
    filtered_records = [
        record for record in SeqIO.parse(input_file, 'fasta')
        if record.id in valid_seq
    ]
    return filtered_records


def extract_low_score_ids(filepath, threshold=90.0, min_threshold = 0):
    """
    Extracts target IDs from a scored alignment file where the score is below a given threshold.

    Args:
        filepath (str): Path to the scored text file.
        threshold (float): Score threshold. Only IDs with scores below this value will be included.

    Returns:
        List[str]: A list of target IDs as strings.
    """
    target_ids_below_threshold = []

    with open(filepath, "r") as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 2:
                target_id, score = parts
                try:
                    if min_threshold< float(score) < threshold:
                        target_ids_below_threshold.append(target_id)
                except ValueError:
                    continue  # skip headers and malformed lines

    return target_ids_below_threshold


def all_seq_present(valid_seq,input_file):
    all_seq_set = {seq.id for seq in SeqIO.parse(input_file, 'fasta')}
    if len(valid_seq - all_seq_set) != 0:
        return False
    return True 
if __name__ == '__main__':
    file_path = r"C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\aligment_data\Seaview\end_nodes\A4_A5\FASTA\less_than_30_scores_A4_A5.txt"
    valid_seq_lst = extract_low_score_ids(file_path, threshold=90.0,min_threshold=0.0)
    valid_seq = set(valid_seq_lst)
    input_file = r"/aligment_data/Seaview/end_nodes/A4_A5/FASTA/alinged_A4_A5_merged_ends"
    error = all_seq_present(valid_seq,input_file)
    if error == False:
        raise ValueError('Sequence ID not found')
    out_name = ''.join(valid_seq_lst)
    output_file = fr'C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\aligment_data\Seaview\end_nodes\A4_A5\FASTA\sub_cluster_less_30_A4_A5_less_than_90.fasta'
    filtered_records = filter_data(input_file,valid_seq)
    save_file(output_file,filtered_records)



