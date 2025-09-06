export module orchestration;

namespace car_app::core {

export class ColtrolOrchestrator {
public:
    ColtrolOrchestrator();

    void start();
    void stop();

private:
    bool running_;
};

} // namespace car_app::core
