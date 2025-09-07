import orchestration;

#include <iostream>
#include <memory>
#include <string>
#include <thread>

#include <grpcpp/grpcpp.h>
#include "movement.pb.h"
#include "movement.grpc.pb.h"
#include "movement/StdInputHandler.h"
#include "dependency_injection/ServiceProvider.h"
#include "movement/CommandDispatcher.h"

using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;
using namespace car_app::core;
using namespace car_ipc;

int main(int argc, char** argv) {
    std::cout << "Starting CarApp " << std::endl;

    std::string target_address = "localhost:50051";
    auto client = MovementClient::NewStub(grpc::CreateChannel(target_address, grpc::InsecureChannelCredentials()));

    ServiceProvider::instance()
        .registerAs<IInputHandler>(std::make_shared<StdInputHandler>())
        .registerAs<ControlOrchestrator>(std::make_shared<ControlOrchestrator>())
        .registerAs<ICommandDispatcher>(std::make_shared<CommandDispatcher>(std::move(client)));
    
    std::thread orchestrator_thread([]() {
        ServiceProvider::instance().get<ControlOrchestrator>()->start();
    });

    const auto handlerCallback = [](const InputCommand& inputCommand) {
        std::cout << "You typed: " << (int) inputCommand << std::endl;
    };

    ServiceProvider::instance().get<IInputHandler>()->start(handlerCallback);
    orchestrator_thread.join();
    
    std::cout << "Finishing CarApp " << std::endl;
    return 0;
}
