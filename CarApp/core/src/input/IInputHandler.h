#pragma once

#include "InputCommand.h"
#include "InputCommandQueue.h"
#include <functional>

namespace car_app::core {

class IInputHandler {
public:
    virtual ~IInputHandler() = default;

    virtual void start() = 0;
    virtual void stop() = 0;

    virtual InputCommandQueue& getInputCommandQueue() = 0;
};

} // namespace car_app::core