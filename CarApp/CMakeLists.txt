# CMake's minimum required version
cmake_minimum_required(VERSION 3.15)

# Define the project name
project(CarApp VERSION 1.0.0 LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_PREFIX_PATH "${CMAKE_PREFIX_PATH};${CMAKE_CURRENT_SOURCE_DIR}/build")


# --- PROTOBUF AND GRPC INTEGRATION ---
# Find Protobuf and gRPC on the system.
# This is required to find the necessary tools for compiling our .proto file.
find_package(protobuf REQUIRED)
find_package(gRPC CONFIG REQUIRED)

# Compile the .proto file into C++ and Python source code.
# This creates a shared library that both applications will use.
PROTOBUF_GENERATE_CPP(proto_sources proto_headers shared_protos/greeter.proto)
add_library(shared_protos STATIC ${proto_sources} ${grpc_sources})
target_include_directories(shared_protos PUBLIC "${CMAKE_CURRENT_BINARY_DIR}")
target_link_libraries(shared_protos PUBLIC protobuf::protobuf gRPC::grpc++)

# --- C++ SUB-PROJECT ---
add_subdirectory(cpp_app)
add_dependencies(cpp_app_executable shared_protos)


# --- PYTHON APPLICATION ---
# Use CMake's ExternalProject to manage the Python app.
# include(ExternalProject)
# ExternalProject_Add(
#     python_app_setup
#     SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/python_app"
#     CONFIGURE_COMMAND ""
#     BUILD_COMMAND ""
#     INSTALL_COMMAND ""
#     STEP_TARGETS install_deps
#     COMMAND
#         ${CMAKE_COMMAND} -E chdir "${CMAKE_CURRENT_SOURCE_DIR}/python_app"
#         poetry install
#     # Ensure the python setup runs after the proto files are generated.
#     DEPENDS
#         "${CMAKE_CURRENT_BINARY_DIR}/greeter_pb2.py"
# )
