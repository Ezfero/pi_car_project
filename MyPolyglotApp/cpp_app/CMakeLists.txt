# Configure the C++ executable
add_executable(cpp_app_executable src/main.cpp)

# Link to C++ dependencies from Conan
target_link_libraries(cpp_app_executable PRIVATE Catch2::Catch2WithMain)
