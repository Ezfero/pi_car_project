import grpc
import time
from concurrent import futures

# Import the generated gRPC files
from ..shared_protos import greeter_pb2
from ..shared_protos import greeter_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class GreeterServicer(greeter_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        print(f"Server received: {request.name}")
        return greeter_pb2.HelloReply(message=f"Hello, {request.name}!")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    greeter_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC server started on port 50051. Press Ctrl+C to stop.")
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    print("Hello from the Python App!")
    serve()
