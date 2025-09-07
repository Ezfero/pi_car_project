export module orchestration;

namespace car_app::core {

export class ControlOrchestrator {
public:
    ControlOrchestrator() = default;

    void start();
    void stop();

private:
    bool running_;
};

} // namespace car_app::core
