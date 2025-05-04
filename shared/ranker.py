
from shared.config import RANK_WEIGHTS

def calculate_rank(metrics):
    return (
        RANK_WEIGHTS["queue_len"] * metrics.get("queue_len", 0) +
        RANK_WEIGHTS["cpu_util"] * metrics.get("cpu_util", 0.0) +
        RANK_WEIGHTS["pending_replications"] * metrics.get("pending_replications", 0) +
        RANK_WEIGHTS["steal_delay"] * metrics.get("steal_delay", 0)
    )
