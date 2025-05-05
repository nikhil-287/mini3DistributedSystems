import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast
import os

# Create output folder
os.makedirs("graphs", exist_ok=True)

# Load benchmark data
benchmark = pd.read_csv("../server/results/benchmark.csv", header=None,
                        names=["RequestID", "Timestamp", "SelectedNodes", "SuccessNodes", "Latency"])
benchmark["Timestamp"] = pd.to_numeric(benchmark["Timestamp"], errors='coerce')
benchmark["SelectedNodes"] = benchmark["SelectedNodes"].apply(ast.literal_eval)
benchmark["SuccessNodes"] = benchmark["SuccessNodes"].apply(ast.literal_eval)
benchmark["Latency"] = pd.to_numeric(benchmark["Latency"], errors='coerce')

# Plot latency per request
plt.figure(figsize=(10, 5))
plt.plot(benchmark["RequestID"], benchmark["Latency"])
plt.xlabel("Request")
plt.ylabel("Latency (s)")
plt.title("Latency per Request")
plt.grid()
plt.savefig("graphs/latency_per_request.png")
plt.close()

# Count frequency of each node being selected and successful
from collections import Counter

all_selected = Counter([node for sublist in benchmark["SelectedNodes"] for node in sublist])
all_success = Counter([node for sublist in benchmark["SuccessNodes"] for node in sublist])

df_freq = pd.DataFrame({
    "Node": list(all_selected.keys()),
    "SelectedCount": [all_selected[k] for k in all_selected],
    "SuccessCount": [all_success.get(k, 0) for k in all_selected]
})

# Barplot for node usage
df_freq.set_index("Node")[["SelectedCount", "SuccessCount"]].plot(kind="bar")
plt.title("Node Selection and Success Frequency")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("graphs/node_usage_barplot.png")
plt.close()

# Load heartbeat log
# Load heartbeat log without headers
heartbeat = pd.read_csv(
    "../server/results/heartbeat_log.csv",
    header=None,
    names=["Timestamp", "NodeID", "QueueLen", "CPUUtil", "PendingReplications", "StealDelay"]
)
heartbeat["Timestamp"] = pd.to_datetime(heartbeat["Timestamp"], unit='s')

sns.lineplot(data=heartbeat, x="Timestamp", y="QueueLen", hue="NodeID")
plt.title("Queue Length Over Time")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("graphs/queue_length_over_time.png")
plt.close()

sns.lineplot(data=heartbeat, x="Timestamp", y="CPUUtil", hue="NodeID")
plt.title("CPU Utilization Over Time")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("graphs/cpu_util_over_time.png")
plt.close()

# Load rank log
rank_log = pd.read_csv("../server/results/rank_log.csv", header=None,
                       names=["RequestID", "NodeID", "RankScore", "Timestamp"])

# Convert timestamp and rank score to proper types
rank_log["Timestamp"] = pd.to_datetime(rank_log["Timestamp"], unit='s')
rank_log["RankScore"] = pd.to_numeric(rank_log["RankScore"], errors='coerce')

# Set up plot style
plt.figure(figsize=(14, 6))
sns.set(style="whitegrid")

# Plot smooth lines for each node
sns.lineplot(
    data=rank_log,
    x="Timestamp",
    y="RankScore",
    hue="NodeID",
    linewidth=2.5,
    marker="o",
    markersize=4,
    alpha=0.8
)

plt.title("Smoothed Rank Score Over Time by Node", fontsize=14)
plt.xlabel("Time", fontsize=12)
plt.ylabel("Rank Score", fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("graphs/rank_score_over_time.png")
plt.close()
