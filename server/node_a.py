import time
import random
import grpc
from concurrent import futures
import time
import threading
import queue
import os
from collections import deque
import replication_pb2 as replication_pb2
import replication_pb2_grpc as replication_pb2_grpc
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from shared import metrics
from shared import ranker
from shared import config

NODE_ID = "A"
REPLICA_IDS = ["B", "C", "D", "E"]
REPLICA_STUBS = {}
PENDING_REPLICATIONS = {}

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
        # Simulate metric gathering; replace with actual RPC if needed
        queue_len = random.randint(0, 10)
        cpu_util = random.uniform(0.1, 0.9)
        pending = PENDING_REPLICATIONS.get(node_id, 0)
        steal_delay = random.randint(0, 10)
        node_metrics[node_id] = {
            "queue_len": queue_len,
            "cpu_util": cpu_util,
            "pending_replications": pending,
            "steal_delay": steal_delay,
        }
    return node_metrics

class ReplicationServicer(replication_pb2_grpc.ReplicationServicer):
    def SendWrite(self, request, context):
        print(f"[{NODE_ID}] Received client request: {request.data}")

        metrics_map = get_metrics()
        ranked = []
        for node_id, m in metrics_map.items():
            score = ranker.calculate_rank(m)
            ranked.append((score, node_id))
        ranked.sort()
        print(ranked)
        selected_nodes = [node_id for _, node_id in ranked[:config.W]]
        print(f"[{NODE_ID}] Selected nodes for replication: {selected_nodes}")

        success_count = 0
        for node_id in selected_nodes:
            try:
                stub = get_stub(node_id)
                response = stub.SendWrite(request)
                if response.success:
                    success_count += 1
                    PENDING_REPLICATIONS[node_id] = PENDING_REPLICATIONS.get(node_id, 0) + 1
            except grpc.RpcError as e:
                print(f"[{NODE_ID}] Error sending to {node_id}: {e}")

        ack = replication_pb2.WriteAck(success=(success_count == config.W), node_id=NODE_ID)
        return ack

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    replication_pb2_grpc.add_ReplicationServicer_to_server(ReplicationServicer(), server)
    server.add_insecure_port(f"[::]:50050")
    server.start()
    print(f"[{NODE_ID}] Server started on port 50050")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
