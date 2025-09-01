import os
import pandas as pd


def walk(dirname):
    for root, _, files in os.walk(dirname):
        for file in files:
            if file.endswith((".csv", ".xlsx")):
                yield file, read_data(os.path.join(root, file))


def read_data(file):
    try:
        data = pd.read_csv(file)
    except Exception:
        data = pd.read_excel(file)
    return data


def count_reads(data):
    return data["ReadsID"].notna().sum()


def average_length(data):
    if "ReadLength" in data.columns:
        return data["ReadLength"].mean()
    else:
        raise ValueError("Length column not found in the data.")


def extract_probe_info(file_name):
    parts = os.path.splitext(file_name)[0].split("_")
    probe1 = "_".join(parts[2:4]) if len(parts) >= 4 else "Error: Probe1 not found"
    probe2 = "_".join(parts[6:8]) if len(parts) >= 8 else "Error: Probe2 not found"
    return probe1, probe2


if __name__ == "__main__":
    dirname = r"C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\hist_data\nanopore_histrogram"
    results = []
    for file_name, data in walk(dirname):
        try:
            probe1, probe2 = extract_probe_info(file_name)
            combined_name = f"{probe1}_vs_{probe2}"
            read_count = count_reads(data)
            avg_length = average_length(data)
            results.append((combined_name, read_count, avg_length))
        except Exception as e:
            probe1, probe2 = extract_probe_info(file_name)
            combined_name = f"{probe1}_vs_{probe2}"
            results.append((combined_name, f"Error: {e}", None))
    df = pd.DataFrame(results, columns=["Probes", "Read Count", "Average Length"])
    df.to_excel("nanopore_hist_summary_results.xlsx", index=False)
