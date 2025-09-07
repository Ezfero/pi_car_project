#pragma once

#include "InputCommand.h"
#include <queue>
#include <mutex>
#include <condition_variable>

namespace car_app::core {

class InputCommandQueue {
public:

    void push(const InputCommand& value);
    InputCommand pop();

private:
    std::queue<InputCommand> queue_;
    mutable std::mutex mutex_;
    std::condition_variable cv_;
};

} // namespace car_app::core