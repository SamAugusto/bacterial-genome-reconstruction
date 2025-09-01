from Bio import SeqIO
import pandas as pd

fastq_file = r"/aligment_data/Fastq/Node_A2_TGG_vs_A3_AGG.fastq"

seq_names = []
avg_scores = []

for record in SeqIO.parse(fastq_file, "fastq"):
    seq_names.append(record.id)
    phred_scores = record.letter_annotations["phred_quality"]
    avg_score = sum(phred_scores) / len(phred_scores) if phred_scores else 0
    avg_scores.append(avg_score)

df = pd.DataFrame({
    "sequence_id": seq_names,
    "average_quality": avg_scores
})

# Save to CSV (optional)
df.to_csv("A2_A3_average_quality_scores.csv", index=False)

print(df)
