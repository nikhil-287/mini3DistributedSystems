
import grpc
import time
import replication_pb2 as replication_pb2
import replication_pb2_grpc as replication_pb2_grpc
from datetime import datetime

NUM_REQUESTS = 5
SERVER_ADDRESS = "localhost:50050"

def send_requests():
    channel = grpc.insecure_channel(SERVER_ADDRESS)
    stub = replication_pb2_grpc.ReplicationStub(channel)

    latencies = []

    for i in range(NUM_REQUESTS):
        data = f"payload-{i}"
        timestamp = datetime.utcnow().isoformat()

        request = replication_pb2.WriteRequest(
            data=data,
            timestamp=timestamp
        )

        start_time = time.time()
        response = stub.SendWrite(request)
        end_time = time.time()

        latency = end_time - start_time
        latencies.append(latency)

        print(f"[Client] Sent: {data}, Success: {response.success}, Latency: {latency:.3f}s")

    avg_latency = sum(latencies) / len(latencies)
    print(f"\nAverage Latency: {avg_latency:.3f}s")

if __name__ == "__main__":
    send_requests()
