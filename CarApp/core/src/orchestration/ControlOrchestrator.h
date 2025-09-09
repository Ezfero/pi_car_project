#pragma once

namespace car_app::core {

class ControlOrchestrator {
public:
    ControlOrchestrator() = default;

    void start();
    void stop();

private:
    bool running_;
};

} // namespace car_app::core
