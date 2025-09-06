#include "CommandDispatcher.h"

namespace car_app::core {

using namespace car_ipc;

CommandDispatcher::CommandDispatcher(std::unique_ptr<car_ipc::MovementClient::Stub> movementClient)
    : movementClient_(std::move(movementClient)) {}
    
CommandDispatcher::~CommandDispatcher() = default;

void CommandDispatcher::forward(const int distance) const {
    MoveRequest request;
    request.set_distance(distance);

    MoveReply reply;
    grpc::ClientContext context;

    grpc::Status status = movementClient_->MoveForward(&context, request, &reply);

    if (!status.ok()) {
        // Handle error
    }
}

void CommandDispatcher::backward(const int distance) const {
    MoveRequest request;
    request.set_distance(distance);

    MoveReply reply;
    grpc::ClientContext context;

    grpc::Status status = movementClient_->MoveBackward(&context, request, &reply);

    if (!status.ok()) {
        // Handle error
    }
}

void CommandDispatcher::left(const int angle) const {
    TurnRequest request;
    request.set_angle(angle);

    TurnReply reply;
    grpc::ClientContext context;

    grpc::Status status = movementClient_->TurnLeft(&context, request, &reply);

    if (!status.ok()) {
        // Handle error
    }
}

void CommandDispatcher::right(const int angle) const {
    TurnRequest request;
    request.set_angle(angle);

    TurnReply reply;
    grpc::ClientContext context;

    grpc::Status status = movementClient_->TurnRight(&context, request, &reply);

    if (!status.ok()) {
        // Handle error
    }
}

}  // namespace car_app::core