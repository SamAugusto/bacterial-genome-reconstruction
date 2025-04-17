
# Bacterial Genome Reconstruction

This repository contains scripts and data for organizing theoretical genome reconstruction from probe-based data. The current focus is on Nanopore sequencing, with future integration of other data types.

## 📁 Repository Structure

- `experimental_data/`: Contains experimental datasets (e.g., filtered hit summaries).
- `theoretical_data/`: Contains theoretical datasets and processing scripts.
  - `nanopore/`: Data and scripts related to Nanopore sequencing.
  - `pacbio/`: Placeholder for future PacBio processing.
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

aaa
python theoretical_data/nanopore/seqkit_node_pairs.py
aaa

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

## ⚙️ Setup

To install required dependencies:

aaa
pip install -r requirements.txt
aaa
