#pragma once

#include "InputCommand.h"
#include <functional>

namespace car_app::core {

class IInputHandler {
public:
    using InputCallback = std::function<void(const InputCommand&)>;

    virtual ~IInputHandler() = default;

    virtual void start(const InputCallback& callback) = 0;
    virtual void stop() = 0;
};

} // namespace car_app::core