import re
import networkx as nx

file_path = "D:\\Dileep\\NIDHI_V02\\correlation_output.txt"

# --- Store values ---
pairs = {}        # cross-correlation edges
auto_corr = {}    # auto-correlation per sequence
sequences = set()

current_pair = None
current_seq = None

with open(file_path, "r") as f:
    for line in f:

        # --- Cross-correlation ---
        seq_match = re.search(r"Sequence (\d+) vs Sequence (\d+)", line)
        cross_mag_match = re.search(r"Peak cross-correlation magnitude:\s*([0-9.]+)", line)

        if seq_match:
            a = int(seq_match.group(1))
            b = int(seq_match.group(2))
            current_pair = (a, b)
            sequences.update([a, b])

        if cross_mag_match and current_pair:
            pairs[current_pair] = float(cross_mag_match.group(1))

        # --- Auto-correlation ---
        auto_seq_match = re.search(r"Sequence (\d+):", line)
        auto_mag_match = re.search(r"Peak auto-correlation magnitude:\s*([0-9.]+)", line)

        if auto_seq_match:
            current_seq = int(auto_seq_match.group(1))
        if auto_mag_match and current_seq is not None:
            auto_corr[current_seq] = float(auto_mag_match.group(1))

# --- Thresholds ---
auto_threshold = float(input("Enter AUTO threshold: "))
cross_threshold = float(input("Enter CROSS threshold: "))

# --- Filter sequences by auto-correlation ---
valid_nodes = [s for s in sequences if auto_corr.get(s, float('inf')) <= auto_threshold]

# --- Build graph using cross-correlation ---
G = nx.Graph()
G.add_nodes_from(valid_nodes)

for (a, b), mag in pairs.items():
    if a in valid_nodes and b in valid_nodes and mag <= cross_threshold:
        G.add_edge(a, b)

# --- Find maximal cliques ---
max_cliques = list(nx.find_cliques(G))
max_cliques = [sorted(c) for c in max_cliques]
max_cliques.sort(key=lambda x: (len(x), x))

# --- Save output ---
out_path = "D:\\Dileep\\NIDHI_V02\\op.txt"
with open(out_path, "w") as f:
    for c in max_cliques:
        line = "{" + ",".join(map(str, c)) + "}-" + str(len(c))
        print(line)
        f.write(line + "\n")