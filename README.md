# 🧬 Bacterial Genome Reconstruction Pipeline

This repository contains a modular Python pipeline developed during my Data Engineering Internship at Drexel University's School of Biomedical Engineering. The tool automates the extraction, processing, and network modeling of overlapping k-mers from long-read sequencing data (e.g., Nanopore, PacBio) for bacterial genome reconstruction.

## 📁 Project Structure

```text
pipeline/
├── Nodes.py                # Organizes node groupings from filtered k-mers
├── KmerCounter.py          # Computes minimum hits from each group
├── kmerList.py             # Generates k-mer summary per sheet
├── sheet_separation.py     # Splits sheets based on unique probe patterns
├── delete_sheets.py        # Removes unnecessary sheets from workbook
```

## 💻 What It Does

- Parses raw Excel files with k-mer hits and probe IDs
- Extracts unique groupings of probes based on pattern matches
- Calculates minimum hits and unique k-mer counts
- Automates sheet creation and workbook cleanup

## 🔧 Tools Used

- Python 3.x
- pandas
- openpyxl
- re (regex)

## 🧪 How to Run

1. Clone the repository
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
3. Place your input file (sequences.xlsx) in the root directory
4. Run scripts in order
  python pipeline/sheet_separation.py
  python pipeline/kmerList.py
  python pipeline/KmerCounter.py
  python pipeline/Nodes.py
  python pipeline/delete_sheets.py

---

### 🧠 Additional Notes

Some logic and automation scripts were co-developed using AI-assisted coding support (ChatGPT) to accelerate pipeline development and documentation.

The data shown in the demo input and sample output files was also generated using ChatGPT and is not based on real laboratory data. However, it follows the same format and structure as the actual sequencing data used during my research at Drexel University.




