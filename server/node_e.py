
import grpc
from concurrent import futures
import time
import threading
import os
from collections import deque
import replication_pb2 as replication_pb2
import replication_pb2_grpc as replication_pb2_grpc
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from shared import metrics, config

NODE_ID = "E"
PORT = config.NODES[NODE_ID].split(":")[1]
QUEUE_PROCESSING_DELAY = 1  # seconds

task_queue = deque()
lock = threading.Lock()

class ReplicationServicer(replication_pb2_grpc.ReplicationServicer):
    def SendWrite(self, request, context):
        with lock:
            task_queue.append(request)
        print(f"[{NODE_ID}] Received write: {{request.data}}")
        return replication_pb2.WriteAck(success=True, node_id=NODE_ID)

    def RequestSteal(self, request, context):
        print(f"[{NODE_ID}] Received steal request from {{request.requester_id}}")
        stolen_tasks = []

        with lock:
            while len(stolen_tasks) < 2 and task_queue:
                stolen_tasks.append(task_queue.popleft())

        print(f"[{NODE_ID}] Sent {{len(stolen_tasks)}} stolen tasks")
        return replication_pb2.StealResponse(stolen_tasks=stolen_tasks)

    def ReportMetrics(self, request, context):
        print(f"[{NODE_ID}] Unexpected call to ReportMetrics.")
        return replication_pb2.WriteAck(success=True, node_id=NODE_ID)

def process_queue():
    while True:
        time.sleep(QUEUE_PROCESSING_DELAY)
        with lock:
            if task_queue:
                task = task_queue.popleft()
                print(f"[{NODE_ID}] Processed task: {{task.data}}")
                save_result(task)

def save_result(task):
    os.makedirs("results", exist_ok=True)
    with open(f"results/{NODE_ID}.log", "a") as f:
        f.write(f"{task.timestamp}: {task.data}\n")

def send_heartbeat():
    while True:
        time.sleep(2)
        queue_len = len(task_queue)
        cpu_util = metrics.get_cpu_util()
        pending_replications = 0
        steal_delay = 0

        try:
            channel = grpc.insecure_channel(config.NODES["A"])
            stub = replication_pb2_grpc.ReplicationStub(channel)
            heartbeat = replication_pb2.MetricsReport(
                node_id=NODE_ID,
                queue_len=queue_len,
                cpu_util=cpu_util,
                pending_replications=pending_replications,
                steal_delay=steal_delay
            )
            stub.ReportMetrics(heartbeat)
        except Exception as e:
            print(f"[{NODE_ID}] Failed to send heartbeat: {{e}}")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    replication_pb2_grpc.add_ReplicationServicer_to_server(ReplicationServicer(), server)
    server.add_insecure_port(f"[::]:{PORT}")
    server.start()
    print(f"[{NODE_ID}] Server started on port {PORT}")
    server.wait_for_termination()

if __name__ == "__main__":
    threading.Thread(target=process_queue, daemon=True).start()
    threading.Thread(target=send_heartbeat, daemon=True).start()
    serve()
