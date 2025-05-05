
from shared.config import RANK_WEIGHTS, HOP_DISTANCE

def calculate_rank(metrics, node_id):
    return (
        RANK_WEIGHTS["queue_len"] * metrics.get("queue_len", 0) +
        RANK_WEIGHTS["cpu_util"] * metrics.get("cpu_util", 0.0) +
        RANK_WEIGHTS["pending_replications"] * metrics.get("pending_replications", 0) +
        RANK_WEIGHTS["steal_delay"] * metrics.get("steal_delay", 0) +
        RANK_WEIGHTS["hop_distance"] * HOP_DISTANCE.get(node_id, 1)
    )
