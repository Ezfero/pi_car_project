#include "InputCommandQueue.h"

namespace car_app::core {

void InputCommandQueue::push(const InputCommand& value) {
    std::lock_guard<std::mutex> lock(mutex_);
    queue_.push(std::move(value));
    cv_.notify_one();
}

InputCommand InputCommandQueue::pop() {
    std::unique_lock<std::mutex> lock(mutex_);
    cv_.wait(lock, [this]{ return !queue_.empty(); });
    InputCommand value = std::move(queue_.front());
    queue_.pop();
    return value;
}

} // namespace car_app::core