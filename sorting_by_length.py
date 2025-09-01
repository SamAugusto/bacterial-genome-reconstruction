import heapq

file_path = r"C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\Scripts\link\A2_A3_allpaths_new_data.txt"

top_25 = []
with open(file_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        # push (length, line)
        heapq.heappush(top_25, (len(line), line))
        if len(top_25) > 25:
            heapq.heappop(top_25)

# Sort final 25 for output
for _, line in sorted(top_25, key=lambda x: (-x[0], x[1])):
    nodes = line.split("→")  # split by arrow
    start_node = nodes[0].strip()
    end_node = nodes[-1].strip()
    print(f"{line}\nStart: {start_node} | End: {end_node}\n")
