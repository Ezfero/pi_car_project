#pragma once

#include <grpcpp/grpcpp.h>
#include "movement.pb.h"
#include "movement.grpc.pb.h"
#include "ICommandDispatcher.h"

namespace car_app::core {

class CommandDispatcher : public ICommandDispatcher {
public:
    explicit CommandDispatcher(
        std::unique_ptr<car_ipc::MovementClient::Stub> movementClient);
    ~CommandDispatcher();

    void forward(const int distance) const override;
    void backward(const int distance) const override;
    void left(const int angle) const override;
    void right(const int angle) const override;
    void stop() const override;

private:
    grpc::ClientContext createContext() const;

    std::unique_ptr<car_ipc::MovementClient::Stub> movementClient_;
};

} // namespace car_app::core
