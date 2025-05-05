
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
    "pending_replications": 1.0,
    "steal_delay": 1.0,
    "hop_distance": 7.0   # significant penalty for being remote
}
#how many replications
W = 2
N = 4

STEAL_THRESHOLD = 5
STEAL_MIN_DELAY = 10

HOP_DISTANCE = {
    "B": 1,
    "C": 1,
    "D": 2,
    "E": 2
}
#here d and e are on machine 2 so more penalty