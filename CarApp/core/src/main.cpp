import orchestration;

#include <iostream>
#include <memory>
#include <string>
#include <thread>

#include <grpcpp/grpcpp.h>
#include "movement.pb.h"
#include "movement.grpc.pb.h"
#include "movement/StdInputHandler.h"

using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;
using car_ipc::Greeter;
using car_ipc::HelloReply;
using car_ipc::HelloRequest;
using namespace car_app::core;

class GreeterClient {
public:
    GreeterClient(std::shared_ptr<Channel> channel)
        : stub_(Greeter::NewStub(channel)) {}

    std::string SayHello(const std::string& user) {
        HelloRequest request;
        request.set_name(user);

        HelloReply reply;
        ClientContext context;

        Status status = stub_->SayHello(&context, request, &reply);

        if (status.ok()) {
            return reply.message();
        } else {
            std::cout << "RPC failed: " << status.error_code() << ": " << status.error_message()
                      << std::endl;
            return "RPC failed";
        }
    }

private:
    std::unique_ptr<Greeter::Stub> stub_;
};

int main(int argc, char** argv) {
    std::cout << "Starting CarApp " << std::endl;
    ControlOrchestrator orchestrator;
    std::thread orchestrator_thread([&orchestrator]() {
        orchestrator.start();
    });

    StdInputHandler handler;
    const auto handlerCallback = [](const InputCommand& inputCommand) {
        std::cout << "You typed: " << (int) inputCommand << std::endl;
    };

    handler.start(handlerCallback);

    orchestrator_thread.join();

    // std::string target_address = "localhost:50051";
    
    // // Create a client and connect to the gRPC server (the Python app)
    // GreeterClient client(grpc::CreateChannel(target_address, grpc::InsecureChannelCredentials()));
    
    // std::string user = "World from C++";
    // std::string reply = client.SayHello(user);
    // std::cout << "Client received: " << reply << std::endl;
    
    std::cout << "Finishing CarApp " << std::endl;
    return 0;
}
