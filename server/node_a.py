import grpc
from concurrent import futures
import threading
import time
import replication_pb2 as replication_pb2
import replication_pb2_grpc as replication_pb2_grpc
import sys
import os
import csv

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from shared import metrics, ranker, config

NODE_ID = "A"
REPLICA_IDS = ["B", "C", "D", "E"]
REPLICA_STUBS = {}
PENDING_REPLICATIONS = {}
LIVE_METRICS = {}

def get_stub(node_id):
    if node_id in REPLICA_STUBS:
        return REPLICA_STUBS[node_id]
    channel = grpc.insecure_channel(config.NODES[node_id])
    stub = replication_pb2_grpc.ReplicationStub(channel)
    REPLICA_STUBS[node_id] = stub
    return stub

def get_metrics():
    node_metrics = {}
    for node_id in REPLICA_IDS:
        m = LIVE_METRICS.get(node_id, {
            "queue_len": 0,
            "cpu_util": 0.0,
            "pending_replications": 0,
            "steal_delay": 0
        })
        m["pending_replications"] = PENDING_REPLICATIONS.get(node_id, 0)
        node_metrics[node_id] = m
    return node_metrics

class ReplicationServicer(replication_pb2_grpc.ReplicationServicer):
    def SendWrite(self, request, context):
        start = time.time()
        print(f"[{NODE_ID}] Received client request: {request.data}")
        metrics_map = get_metrics()
        ranked = []
        rank_scores = {}

        for node_id, m in metrics_map.items():
            score = ranker.calculate_rank(m, node_id)
            print(f"[{NODE_ID}] Node {node_id} -> Rank Score: {score:.2f} | Metrics: {m}")
            ranked.append((score, node_id))
            rank_scores[node_id] = score

        ranked.sort()

        success_count = 0
        selected_nodes = []
        success_nodes = []

        for _, node_id in ranked:
            if success_count >= config.W:
                break
            try:
                stub = get_stub(node_id)
                response = stub.SendWrite(request)
                if response.success:
                    success_count += 1
                    selected_nodes.append(node_id)
                    success_nodes.append(node_id)
                    PENDING_REPLICATIONS[node_id] = PENDING_REPLICATIONS.get(node_id, 0) + 1
            except grpc.RpcError as e:
                print(f"[{NODE_ID}] Error sending to {node_id}: {e}")
                selected_nodes.append(node_id)

        print(f"[{NODE_ID}] Final selected nodes for replication: {success_nodes}")
        end = time.time()
        latency = end - start

        os.makedirs("results", exist_ok=True)
        with open("results/benchmark.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([request.data, start, selected_nodes, success_nodes, f"{latency:.4f}"])

        with open("results/rank_log.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            for node_id, score in rank_scores.items():
                writer.writerow([request.data, node_id, f"{score:.4f}", start])

        ack = replication_pb2.WriteAck(success=(success_count == config.W), node_id=NODE_ID)
        return ack

    def ReportMetrics(self, request, context):
        LIVE_METRICS[request.node_id] = {
            "queue_len": request.queue_len,
            "cpu_util": request.cpu_util,
            "pending_replications": request.pending_replications,
            "steal_delay": request.steal_delay
        }

        os.makedirs("results", exist_ok=True)
        with open("results/heartbeat_log.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                time.time(),
                request.node_id,
                request.queue_len,
                f"{request.cpu_util:.4f}",
                request.pending_replications,
                request.steal_delay
            ])

        return replication_pb2.WriteAck(success=True, node_id=NODE_ID)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    replication_pb2_grpc.add_ReplicationServicer_to_server(ReplicationServicer(), server)
    server.add_insecure_port(f"[::]:50050")
    server.start()
    print(f"[{NODE_ID}] Server started on port 50050")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
