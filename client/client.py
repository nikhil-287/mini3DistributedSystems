import grpc
import replication_pb2 as replication_pb2
import replication_pb2_grpc as replication_pb2_grpc
import time
import csv
from datetime import datetime


NUM_REQUESTS = 100
NODE_A_ADDRESS = "localhost:50050"

def main():
    channel = grpc.insecure_channel(NODE_A_ADDRESS)
    stub = replication_pb2_grpc.ReplicationStub(channel)

    with open("../server/results/client_log.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["RequestID", "Timestamp", "Data"])

        for i in range(NUM_REQUESTS):
            data = f"payload-{i}"
            timestamp = datetime.utcnow().isoformat()
            request = replication_pb2.WriteRequest(data=data, timestamp=timestamp)
            try:
                response = stub.SendWrite(request)
                if response.success:
                    print(f"[CLIENT] Sent: {data} | Ack from {response.node_id}")
                else:
                    print(f"[CLIENT] Failed to write: {data}")
            except grpc.RpcError as e:
                print(f"[CLIENT] gRPC error: {e}")

            writer.writerow([i, timestamp, data])
            time.sleep(0.05)  # slight delay to simulate realistic load

if __name__ == "__main__":
    main()