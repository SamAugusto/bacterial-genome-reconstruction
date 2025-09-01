from Bio import SeqIO
from Bio import Align
import pandas as pd

# Aligment Config
aligner = Align.PairwiseAligner()
aligner.mode = "global"
aligner.mismatch_score = -10


def parse_fasta(file_path, references=None, filter_by_references=False):

    sequences = {}
    for record in SeqIO.parse(file_path, "fasta"):
        if filter_by_references:
            if record.id in references:
                sequences[record.id] = str(record.seq)
            else:
                continue
        else:
            sequences[record.id] = str(record.seq)

    return sequences


def reference_score_calculator(sequences, reference_id, ref_seq):
    score = {}

    reference = ref_seq
    for name, seq in sequences.items():
        penalty = sum(1 for a, b in zip(seq, reference) if a != b)
        print(f"Sequence: lenght {len(seq)}, Reference: {len(reference)}")
        match_score = 100 * ((len(seq) - penalty) / len(seq))
        score[name] = match_score

    return score


def gap_counter(sequence):
    gaps = sequence.count("-")
    return gaps


def pair_alignment(fasta_file, reference):
    aligment_result = {}
    parsed_sequences = parse_fasta(fasta_file)

    for parsed_sequences_id, parsed_sequences_seq in parsed_sequences.items():

        alignments = aligner.align(reference, parsed_sequences_seq)
        aligment_result[parsed_sequences_id] = alignments

    return aligment_result


def mis_match_counter(sequence, reference):
    mismatches = sum(
        1 for a, b in zip(sequence, reference) if a != b and a != "-" and b != "-"
    )
    return mismatches


def process_data(references, reads):
    alignment_data = []
    for reference_name, reference_seq in references.items():
        pre_scored_sequences = pair_alignment(reads, reference_seq)
        alignment_data.append({reference_name: pre_scored_sequences})
    return alignment_data


def creating_df(alignment_data):
    data = {
        "reference_id": [],
        "sequence_id": [],
        "gap_counts": [],
        "mismatch_counts": [],
        "score": [],
    }

    for ref_dict in alignment_data:  # each item in the list
        for ref_id, reads_dict in ref_dict.items():  # reference id and its reads
            for (
                read_id,
                alignments,
            ) in reads_dict.items():  # read id and alignment object
                best_alignment = alignments[0]  # first (best) alignment

                # get raw sequences (without gaps from aligner)
                seq_a = str(best_alignment.sequences[0])
                seq_b = str(best_alignment.sequences[1])

                data["reference_id"].append(ref_id)
                data["sequence_id"].append(read_id)
                data["gap_counts"].append(gap_counter(seq_b))
                data["mismatch_counts"].append(mis_match_counter(seq_b, seq_a))
                data["score"].append(best_alignment.score)

    df = pd.DataFrame(data)
    return df


if __name__ == "__main__":
    # Change the file paths and references as needed
    a2_a3_reads = r"C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\aligment_data\Fasta\Node_A2_TGG_vs_A3_AGG.fasta"
    reference_file_path = r"C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\aligment_data\merged_24_references.fasta"
    references = {
        "Hflu_mpi1117_ctg1",
        "Hflu_mpi993_ctg1",
        "Hflu_mpi1430_ctg1",
        "Hflu_mpi1474_ctg1",
        "Hflu_mpi989_ctg1",
        "Hflu_86_028NP_ctg1",
        "Hflu_mpi1200_ctg1",
        "Hflu_PittGG_ctg1",
        "Hflu_mpi1763_ctg1",
        "Hflu_Hi375_ctg1",
        "Hflu_Rd_KW20_ctg1",
    }
    reference_sequences = parse_fasta(
        reference_file_path, references, filter_by_references=True
    )

    aligned_sequences = process_data(reference_sequences, a2_a3_reads)
    final_df = creating_df(aligned_sequences)
    final_df.to_excel("sequence_alignment_results_pacbio.xlsx", index=False)
