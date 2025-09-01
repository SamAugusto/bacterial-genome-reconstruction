from score_sequence import sequence_parser
from Bio.Align import substitution_matrices, PairwiseAligner
from itertools import combinations
from multiprocessing import Pool, cpu_count
import os

def create_aligner():
    aligner = PairwiseAligner()
    aligner.mode = 'local'
    aligner.substitution_matrix = substitution_matrices.load("BLOSUM62")
    aligner.open_gap_score = -10
    aligner.extend_gap_score = -1
    return aligner

# Include full alignment + score output
def compute_full_output(args):
    id1, id2, seq1, seq2, self1, self2 = args
    aligner = create_aligner()
    score = aligner.score(seq1, seq2)
    alignment = aligner.align(seq1, seq2)[0]
    max_possible = min(self1, self2)
    norm_score = (score / max_possible * 100) if max_possible else 0
    name1 = id1.split('/')[1]
    name2 = id2.split('/')[1]
    return f"{name1} vs {name2} | Raw Score: {score:.2f}, Normalized: {norm_score:.2f}%\n{alignment}\n"

if __name__ == '__main__':
    file = r"C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\aligment_data\Fasta\Node_A2_TGG_vs_A3_AGG.fasta"
    sequences = sequence_parser(file)

    # Precompute self scores
    aligner = create_aligner()
    self_scores = {id_: aligner.score(seq, seq) for id_, seq in sequences.items()}

    jobs = [
        (id1, id2, sequences[id1], sequences[id2], self_scores[id1], self_scores[id2])
        for (id1, id2) in combinations(sequences.keys(), 2)
    ]

    print(f"Prepared {len(jobs)} jobs...")

    with Pool(cpu_count()) as pool:
        results = pool.map(compute_full_output, jobs)

    output_path = "optmized_local_alignment_A2_A3.txt"
    with open(output_path, "w") as f:
        f.write("Local alignment of the consensus data:\n\n")
        f.writelines(results)

    print(f" Done! Results written to {output_path}")
