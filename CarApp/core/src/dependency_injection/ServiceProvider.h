#pragma once

#include <memory>
#include <string>
#include <unordered_map>
#include <typeindex>

namespace car_app::core {

class ServiceProvider {
public:
    static ServiceProvider& instance() {
        static ServiceProvider instance;
        return instance;
    }

    template<typename Base, typename Impl>
    ServiceProvider& registerAs(std::shared_ptr<Impl> service) {
        static_assert(std::is_base_of_v<Base, Impl>, "Derived must inherit from Base");
        services_[std::type_index(typeid(Base))] = std::move(service);
        return *this;
    }

    template<typename T>
    std::shared_ptr<T> get() const {
        auto it = services_.find(std::type_index(typeid(T)));
        if (it == services_.end()) {
            throw std::runtime_error("Service not found");
        }
        return std::static_pointer_cast<T>(it->second);
    }

    template<typename T>
    void unregister() {
        services_.erase(std::type_index(typeid(T)));
    }

    ServiceProvider(const ServiceProvider&) = delete;
    ServiceProvider& operator=(const ServiceProvider&) = delete;

private:
    std::unordered_map<std::type_index, std::shared_ptr<void>> services_;

    ServiceProvider() = default;
};

} // namespace car_app::core