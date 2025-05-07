# Bacterial Genome Reconstruction

This repository contains scripts and data for organizing theoretical genome reconstruction from probe-based data. The current focus is on Nanopore sequencing, with future integration of other data types such as PacBio and human genome simulations.

## 📁 Repository Structure

- `experimental_data/`: Contains experimental datasets (e.g., filtered hit summaries).
- `theoretical_data/`: Contains theoretical datasets and processing scripts.
  - `nanopore/`: Data and scripts related to Nanopore sequencing.
  - `pacbio/`:  PacBio processing scripts and outputs.
  - `human/`: Placeholder for future human genome processing.
- `comparisons/`: Scripts and outputs used for verifying node matches.
- `graphs/`: (To be populated after final comparisons)
- `scripts/`: Python modules used for data preprocessing and validation.
- `requirements.txt`: Python dependencies.

---

## ✅ Experimental Data

Place your experimental datasets (e.g., `final_min_hit_summary.xlsx`) in the `experimental_data/` directory.

---

## 🔬 Theoretical Data Processing: Nanopore

The pipeline processes Nanopore probe `.csv` files to compute distances between probes and determine node pairings based on direction and distance rules.

1. Place raw CSV files in:

   `theoretical_data/nanopore/input/`

2. Run the processing script:

```bash
python theoretical_data/nanopore/seqkit_node_pairs.py
```

3. Output files will be saved to:

   `theoretical_data/nanopore/output/`

Each result includes a `node_pairs` column with format:

```
pattern1,pattern2_seqID
```

---

## 🧱 Remodeled Data Processing

The following scripts read and remodel `*_updated.csv` outputs to structured Excel files.

### 🧬 For Nanopore:
```bash
python scripts/nanopore_sub_node_design.py
```

### 🧬 For PacBio:
```bash
python scripts/pacbio_sub_node_design.py
```

Outputs:
- `nanopore_remodeled_data_design.xlsx`
- `pacbio_remodeled_data_design.xlsx`

Each file includes:
- `Full Data` (remodeled `node_pairs`, `distance`, `source_file`)
- `Unique Nodes` (deduplicated node identifiers)

---

## 🔄 Additional Processing

### 📌 Add Sorted All-Nodes Column

```bash
python scripts/columno_remodeled_design.py
```

Adds an `all_nodes` column with sorted `_`-joined identifiers.

---

### 🧼 Remove Duplicate Node Pairs

```bash
python scripts/remove_node_duplicates.py
```

Ensures entries like `2_90` and `90_2` are only kept once.

---

## 🧪 Sample Demo Files

For testing purposes, fake files are available:

- `synthetic_ctg1_pairs_updated_FAKE.csv`
- `nanopore_remodeled_data_design_FAKE.xlsx`

These help demonstrate how the scripts process actual input/output structures.

---

## ⚙️ Setup

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

## 🤝 Acknowledgment

This project was developed with technical guidance provided via ChatGPT to structure, script, and organize theoretical genome reconstruction workflows, with continuous motivation from Tina 💙.

---

## ⚠️ Data Disclaimer

All data is **synthetic and theoretical**, created to simulate genome reconstruction pipelines. No experimental or clinical sequences are represented unless explicitly stated.
