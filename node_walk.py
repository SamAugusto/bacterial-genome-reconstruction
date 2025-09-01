from Bio import Phylo
from itertools import combinations

# Load tree and sequences
tree = Phylo.read(r"C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\aligment_data\Seaview\double_sided\Aligned\Phylo-Trees\Aligned_240bp_double_sided_trim_A2_A3_trimmed-PhyML_tree", "newick")
sequences = [clade.name for clade in tree.get_terminals() if clade.name]

# Compute all pairwise distances
distances = {
    (s1, s2): tree.distance(s1, s2)
    for s1, s2 in combinations(sequences, 2)
}

# Initialize disjoint sets for clustering
parent = {s: s for s in sequences}

def find(s):
    while parent[s] != s:
        parent[s] = parent[parent[s]]
        s = parent[s]
    return s

def union(s1, s2):
    root1 = find(s1)
    root2 = find(s2)
    if root1 != root2:
        parent[root2] = root1

# Union sequences that are within 0.03
for (s1, s2), dist in distances.items():
    if dist <= 0.014:
        union(s1, s2)

# Group sequences by root parent
from collections import defaultdict
strain_clusters = defaultdict(list)
for s in sequences:
    root = find(s)
    strain_clusters[root].append(s)

# Print resulting strain groups
for i, (strain, members) in enumerate(strain_clusters.items(), 1):
    print(f"Strain {i}: {members}")


#Streamlit file
#
# import streamlit as st
# from Bio import SeqIO
# from Bio.SeqUtils import gc_fraction
# from Bio import Entrez
# from Bio.SeqRecord import SeqRecord
# from collections import Counter
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import gzip
# import io
# import nest_asyncio
# import random
# from Bio import Phylo
# import tempfile
# import matplotlib.pyplot as plt
# import matplotlib
# from io import StringIO
# from itertools import combinations
# from collections import defaultdict
#
# # Required to avoid asyncio loop conflict in Streamlit
# nest_asyncio.apply()
#
# # Set NCBI email for legal API use
# Entrez.email = "samaugusto121@gmail.com"  # ← Replace with your email
#
# st.title("FASTQ/FASTA & NCBI Sequence Viewer")
#
# # -------------------------
# # Upload FASTQ Section
# # -------------------------
# uploaded_file = st.file_uploader("Upload a FASTQ file")
#
#
# def analyze_record(record):
#     with st.expander(f"Read {record.id}", expanded=True):
#         st.code(str(record.seq))
#         data = Counter(record.seq)
#         st.markdown("### Nucleotide Frequency")
#         colors = ['#818D81', '#3C2A33', '#D3C9AC', '#E1702B']
#         st.bar_chart(data, x_label='Nucleotides', y_label='Frequency', color=random.choice(colors))
#
#         gc = 100 * gc_fraction(record.seq)
#         st.write(f"**GC Content**: {gc:.2f}%")
#
#         if "phred_quality" in record.letter_annotations:
#             qualities = record.letter_annotations["phred_quality"]
#             avg_quality = sum(qualities) / len(qualities)
#             st.write(f"The average quality of Read **{record.id}** is: **{avg_quality:.2f}**")
#
#
# # Process uploaded file
# if uploaded_file is not None:
#     st.success(f"Uploaded file: {uploaded_file.name}")
#
#     if uploaded_file.name.endswith(".gz"):
#         with gzip.open(uploaded_file, "rt") as handle:
#             for i, record in enumerate(SeqIO.parse(handle, "fastq")):
#                 analyze_record(record)
#                 if i >= 50: break
#     else:
#         text_stream = io.TextIOWrapper(uploaded_file, encoding='utf-8')
#         try:
#             for i, record in enumerate(SeqIO.parse(text_stream, "fastq")):
#                 analyze_record(record)
#                 if i >= 50: break
#         except Exception:
#             text_stream.seek(0)  # Reset stream
#             for i, record in enumerate(SeqIO.parse(text_stream, "fasta")):
#                 analyze_record(record)
#                 if i >= 50: break
# # -------------------------
# # Alignment Scoring Section
# # -------------------------
# st.markdown("##  Upload Pre-Aligned FASTA File for Alignment Scoring")
# aligned_file = st.file_uploader("Upload Pre-Aligned FASTA File", key="aligned")
#
# if aligned_file is not None:
#     st.success(f"Uploaded alignment file: {aligned_file.name}")
#     aligned_stream = io.TextIOWrapper(aligned_file, encoding='utf-8')
#
#     sequences = {}
#     try:
#         for record in SeqIO.parse(aligned_stream, "fasta"):
#             sequences[record.id] = record.seq
#     except Exception as e:
#         st.error(f"Error parsing FASTA file: {e}")
#         sequences = {}
#
#     if sequences:
#         # Choose the first non-Consensus sequence as reference
#         reference_id = None
#         for name in sequences:
#             if not name.lower().startswith("consensus"):
#                 reference_id = name
#                 break
#
#         if reference_id:
#             def score_calculator(sequences, reference_id):
#                 score = {}
#                 reference = sequences[reference_id]
#                 for name, seq in sequences.items():
#                     if name.lower().startswith("consensus"):
#                         continue  # Skip consensus sequences
#                     if name == reference_id:
#                         score[name] = 100.0  # Perfect self-alignment
#                         continue
#                     penalty = sum(1 for a, b in zip(seq, reference) if a != b)
#                     weight = 15
#                     match_score = 100 * ((len(seq) - penalty * weight) / len(seq))
#                     score[name] = match_score
#                 return score
#
#
#             st.markdown("### Alignment Score Results")
#             st.write(f"**Reference:** {reference_id}")
#
#             scores = score_calculator(sequences, reference_id)
#             score_df = pd.DataFrame(scores.items(), columns=["Sequence ID", "Alignment Score (%)"])
#             st.dataframe(score_df.sort_values(by="Alignment Score (%)", ascending=False), use_container_width=True)
#         else:
#             st.warning("No suitable reference sequence found for scoring.")
#
# # -------------------------
# # NCBI Gene URL Search
# # -------------------------
# st.markdown("## Or Search by NCBI Gene URL")
# search_url = st.text_input("Paste NCBI Gene URL here:")
#
#
# def extract_gene_id_from_url(url):
#     # Attempt to parse Gene ID from typical NCBI Gene URL
#     import urllib.parse
#     parsed = urllib.parse.urlparse(url)
#     query = urllib.parse.parse_qs(parsed.query)
#     term = query.get("Term") or query.get("id") or []
#     return term[0] if term else None
#
#
# def fetch_ncbi_fasta_by_gene_id(gene_id):
#     try:
#         # Search for linked nucleotide record(s)
#         search_handle = Entrez.elink(dbfrom="gene", db="nucleotide", id=gene_id, linkname="gene_nuccore_refseqrna")
#         link_result = Entrez.read(search_handle)
#         search_handle.close()
#
#         linksets = link_result[0]['LinkSetDb']
#         if not linksets:
#             return None
#
#         nucleotide_id = linksets[0]['Link'][0]['Id']
#
#         # Fetch the sequence from NCBI Nucleotide DB
#         fetch_handle = Entrez.efetch(db="nucleotide", id=nucleotide_id, rettype="fasta", retmode="text")
#         seq_record = SeqIO.read(fetch_handle, "fasta")
#         fetch_handle.close()
#         return seq_record
#     except Exception as e:
#         st.error(f"Error fetching from NCBI: {e}")
#         return None
#
#
# # Trigger fetch if a URL is entered
# if search_url:
#     gene_id = extract_gene_id_from_url(search_url)
#     if gene_id:
#         st.info(f"Fetching gene ID: {gene_id}")
#         seq_record = fetch_ncbi_fasta_by_gene_id(gene_id)
#         if seq_record:
#             st.success(f"Successfully fetched: {seq_record.id}")
#             analyze_record(seq_record)
#         else:
#             st.warning("No linked nucleotide sequence found for this gene.")
#     else:
#         st.error("Could not extract a valid gene ID from the URL.")
#
# matplotlib.use("Agg")  # Required for Streamlit to render matplotlib
#
# # -------------------------
# # Phylogenetic Tree Strain Clustering
# # -------------------------
# st.markdown("## Phylogenetic Tree-Based Strain Clustering")
# tree_file = st.file_uploader("Upload Newick-format Phylogenetic Tree", key="tree")
# distance_cutoff = st.number_input("Set branch length cutoff (e.g., 0.03 for 97% similarity)", min_value=0.0,
#                                   max_value=1.0, value=0.03, step=0.001, format="%.3f")
#
# if tree_file is not None:
#     st.success(f"Uploaded tree file: {tree_file.name}")
#     try:
#         tree_data = tree_file.read().decode("utf-8")
#         tree = Phylo.read(StringIO(tree_data), "newick")
#
#         sequences = [clade.name for clade in tree.get_terminals() if clade.name]
#
#         distances = {
#             (s1, s2): tree.distance(s1, s2)
#             for s1, s2 in combinations(sequences, 2)
#         }
#
#         parent = {s: s for s in sequences}
#
#
#         def find(s):
#             while parent[s] != s:
#                 parent[s] = parent[parent[s]]
#                 s = parent[s]
#             return s
#
#
#         def union(s1, s2):
#             root1 = find(s1)
#             root2 = find(s2)
#             if root1 != root2:
#                 parent[root2] = root1
#
#
#         for (s1, s2), dist in distances.items():
#             if dist <= distance_cutoff:
#                 union(s1, s2)
#
#         strain_clusters = defaultdict(list)
#         for s in sequences:
#             root = find(s)
#             strain_clusters[root].append(s)
#
#         st.markdown("### Identified Strain Clusters")
#         for i, (root, members) in enumerate(strain_clusters.items(), 1):
#             st.write(f"**Strain {i}**: {', '.join(members)}")
#
#     except Exception as e:
#         st.error(f"Error processing tree: {e}")