#pragma once

#include <grpcpp/grpcpp.h>
#include "movement.pb.h"
#include "movement.grpc.pb.h"

namespace car_app::core {

class CommandDispatcher {
public:
    explicit CommandDispatcher(
        std::unique_ptr<car_ipc::MovementClient::Stub> movementClient);
    ~CommandDispatcher();

    void forward(const int distance) const;
    void backward(const int distance) const;
    void left(const int angle) const;
    void right(const int angle) const;
    void stop() const;

private:
    grpc::ClientContext createContext() const;

    std::unique_ptr<car_ipc::MovementClient::Stub> movementClient_;
};

} // namespace car_app::core
