
NODES = {
    "A": "localhost:50050",
    "B": "localhost:50051",
    "C": "localhost:50052",
    "D": "localhost:50053",
    "E": "localhost:50054"
}

RANK_WEIGHTS = {
    "queue_len": 2.0,
    "cpu_util": 1.5,
    "pending_replications": 1.2,
    "steal_delay": 1.0
}

W = 2
N = 4

STEAL_THRESHOLD = 5
STEAL_MIN_DELAY = 10

HOP_DISTANCE = {
    "B": 1,
    "C": 2,
    "D": 1,
    "E": 3
}
