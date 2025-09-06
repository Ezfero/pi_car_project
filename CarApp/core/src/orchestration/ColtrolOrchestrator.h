#pragma once

namespace car_app::core {

class ColtrolOrchestrator {
public:
    ColtrolOrchestrator();

    void start();
    void stop();

private:
    bool running_;
};

} // namespace car_app::core
