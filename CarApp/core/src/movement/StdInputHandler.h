#pragma once

#include "IInputHandler.h"

namespace car_app::core {

class StdInputHandler : public IInputHandler {
public:
    StdInputHandler() = default;
    ~StdInputHandler() override = default;

    void start(const InputCallback& callback) override;
    void stop() override;

private:
    const std::unordered_map<char, InputCommand> kCommandsMap = {
        {'w', InputCommand::FORWARD},
        {'s', InputCommand::BACKWARD},
        {'a', InputCommand::LEFT},
        {'d', InputCommand::RIGHT},
        {' ', InputCommand::STOP},
        {'\n', InputCommand::INTERRUPT},
    };

    bool running_;

    char nextChar() const;
};

} // namespace car_app::core