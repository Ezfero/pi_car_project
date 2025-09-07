#pragma once

namespace car_app::core {

class ICommandDispatcher {
public:

    virtual void forward(const int distance) const = 0;
    virtual void backward(const int distance) const = 0;
    virtual void left(const int angle) const = 0;
    virtual void right(const int angle) const = 0;
    virtual void stop() const = 0;

};

} // namespace car_app::core
