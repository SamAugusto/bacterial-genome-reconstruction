from itertools import combinations
from score_sequence import sequence_parser
from Bio.Align import substitution_matrices, PairwiseAligner

def normalized_local_score(score, seq1, seq2, aligner):
    self_score1 = aligner.score(seq1, seq1)
    self_score2 = aligner.score(seq2, seq2)
    max_possible = min(self_score1, self_score2)
    return (score / max_possible * 100) if max_possible else 0

if __name__ == '__main__':
    file = input('Insert the desired file for local alignment: ')
    sequences_to_be_aligned = sequence_parser(file)
    print(sequences_to_be_aligned)

    aligner = PairwiseAligner()
    aligner.mode = 'local'
    aligner.substitution_matrix = substitution_matrices.load("BLOSUM62")
    aligner.open_gap_score = -10
    aligner.extend_gap_score = -1

    with open("optmized_local_alignment_A2_A3.txt", "a") as file1:
        file1.write("Local alignment of the consensus data:\n\n")
        for (id1, seq1), (id2, seq2) in combinations(sequences_to_be_aligned.items(), 2):
            score = aligner.score(seq1, seq2)
            alignment = aligner.align(seq1, seq2)
            normalized_score = normalized_local_score(score, seq1, seq2, aligner)
            file1.write(f"{id1.split('/')[1]} vs {id2.split('/')[1]} | Raw Score: {score:.2f}, Normalized: {normalized_score:.2f}%\n")
            file1.write(f"{alignment[0]}\n\n")
