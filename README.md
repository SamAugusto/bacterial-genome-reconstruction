# Bacterial Genome Reconstruction

This repository contains scripts and data for organizing theoretical genome reconstruction from probe-based data. The current focus is on Nanopore sequencing, with future integration of other data types.

## 📁 Repository Structure

- `experimental_data/`: Contains experimental datasets (e.g., filtered hit summaries).
- `theoretical_data/`: Contains theoretical datasets and processing scripts.
  - `nanopore/`: Data and scripts related to Nanopore sequencing.
  - `pacbio/`:  PacBio processing.
  - `human/`: Placeholder for future Human genome processing.
- `comparisons/`: (To be used after node verification)
- `graphs/`: (To be populated after final comparisons)
- `scripts/`: Additional utility scripts.
- `requirements.txt`: Python dependencies.

## ✅ Experimental Data

Place your experimental datasets (e.g., `final_min_hit_summary.xlsx`) in the `experimental_data/` directory.

## 🔬 Theoretical Data Processing: Nanopore

The current pipeline processes Nanopore probe `.csv` files to compute distances between probes and determine node pairings based on direction and distance rules.

1. Place raw CSV files in:

   `theoretical_data/nanopore/input/`

2. Run the processing script:

```
python theoretical_data/nanopore/seqkit_node_pairs.py
```

3. Output files will be saved to:

   `theoretical_data/nanopore/output/`

Each result includes a `node_pairs` column with format:

```
pattern1,pattern2_seqID
```

Blank rows are inserted to maintain row alignment.

## 📝 Notes

- This stage processes only Nanopore data.
- Distance and orientation rules are used to generate theoretical pairings.
- All results are saved in matching `.csv` formats.
- Additional sequencing types and comparison steps will follow in future phases.

## 🧪 Node Pair Comparison Module (Nanopore & PacBio)

The `scripts/node_comparisson.py` script processes the last column from `_updated.csv` files,
extracts probe pairings, removes genomic suffixes, and compares them with a reference summary file (e.g., `BlatsnSummary.csv`).

Outputs (saved locally, not included in repo):
- `pacbio_unique_nodes.xlsx`
- `nanopore_unique_nodes.xlsx`
- `combined_pacbio_nodes.xlsx`
- `combined_nanopore_nodes.xlsx`

## 📁 Sample Input

A dummy file is included at `data/sample_pairs_updated.csv` to demonstrate the structure expected by `node_comparisson.py`.

It includes:
- Last-column combinations with suffixes (e.g., `-Hflu_dummy_ctg1`)
- Multiple columns to simulate typical `_updated.csv` content

To run:
```bash
python scripts/node_comparisson.py
```

## ⚙️ Setup

To install required dependencies:

```
pip install -r requirements.txt
```

### 🤝 Acknowledgment

This project was developed with the help of technical guidance provided through ChatGPT to assist with structuring, scripting, and organizing theoretical genome reconstruction pipelines.

### ⚠️ Data Disclaimer

All data used in this repository was generated through **theoretical and computational simulations** based on probe sequences. It does **not represent experimental or in-lab generated biological data**, and should be interpreted as such unless explicitly stated otherwise.
