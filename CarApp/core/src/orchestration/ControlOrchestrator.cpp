module;

#include "dependency_injection/ServiceProvider.h"
#include "input/IInputHandler.h"
#include "movement/ICommandDispatcher.h"

module orchestration;

namespace car_app::core {

void ControlOrchestrator::start() {
    running_ = true;
    while (running_) {
        auto command = ServiceProvider::instance().get<IInputHandler>()->getInputCommandQueue().pop();
        auto dispatcher = ServiceProvider::instance().get<ICommandDispatcher>();
        switch (command) {
            case InputCommand::FORWARD:
                dispatcher->forward(1);
                break;
            case InputCommand::BACKWARD:
                dispatcher->backward(0);
                break;
            case InputCommand::LEFT:
                dispatcher->left(15);
                break;
            case InputCommand::RIGHT:
                dispatcher->right(15);
                break;
            case InputCommand::STOP:
                dispatcher->stop();
                break;
            case InputCommand::INTERRUPT:
                running_ = false;
                break;
            default:
                break;
        }
    }
}

void ControlOrchestrator::stop() {
}
} // namespace car_app::core