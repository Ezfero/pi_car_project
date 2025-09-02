# Configure the C++ executable
add_executable(cpp_app_executable src/main.cpp)

# Link to C++ dependencies from Conan and our shared library
target_link_libraries(cpp_app_executable
    PRIVATE
    apis
    gRPC::grpc++
    protobuf::protobuf
)
