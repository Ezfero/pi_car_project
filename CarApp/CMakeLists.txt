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

# --- C++ SUB-PROJECT ---
add_subdirectory(cpp_app)
add_subdirectory(apis)
add_dependencies(cpp_app_executable apis)


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
