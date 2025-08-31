# CMake's minimum required version
cmake_minimum_required(VERSION 3.15)

# Define the project name
project(CarApp VERSION 1.0.0 LANGUAGES CXX)

# --- CONAN INTEGRATION (C++ DEPENDENCIES) ---
# Find Conan and configure a new install folder.
# This ensures that Conan's generated files are separate from the build.
find_package(Conan REQUIRED)
conan_cmake_configure(
    REQUIRES
        catch2/3.4.0
        # gRPC and Protobuf are necessary for inter-process communication
        grpc/1.54.3
        protobuf/3.21.12
    GENERATORS
        CMakeToolchain
        CMakeDeps
    BUILD
        missing
)

# --- PROTOBUF AND GRPC INTEGRATION ---
# Find Protobuf and gRPC on the system.
# This is required to find the necessary tools for compiling our .proto file.
find_package(Protobuf REQUIRED)
find_package(gRPC REQUIRED)

# Compile the .proto file into C++ and Python source code.
# This creates a shared library that both applications will use.
PROTOBUF_GENERATE_CPP(proto_sources proto_headers shared_protos/greeter.proto)
GRPC_CPP_GENERATE_CPP(grpc_sources grpc_headers shared_protos/greeter.proto)
# Create a shared library from the generated C++ files.
add_library(shared_protos STATIC ${proto_sources} ${grpc_sources})
target_include_directories(shared_protos PUBLIC "${CMAKE_CURRENT_BINARY_DIR}")
target_link_libraries(shared_protos PUBLIC Protobuf::libprotobuf gRPC::grpc++)
# This ensures that our `shared_protos` library is built first.
add_dependencies(cpp_app_executable shared_protos)


# --- C++ SUB-PROJECT ---
add_subdirectory(cpp_app)

# --- PYTHON APPLICATION ---
# Use CMake's ExternalProject to manage the Python app.
include(ExternalProject)
ExternalProject_Add(
    python_app_setup
    SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/python_app"
    CONFIGURE_COMMAND ""
    BUILD_COMMAND ""
    INSTALL_COMMAND ""
    STEP_TARGETS install_deps
    COMMAND
        ${CMAKE_COMMAND} -E chdir "${CMAKE_CURRENT_SOURCE_DIR}/python_app"
        poetry install
    # Ensure the python setup runs after the proto files are generated.
    DEPENDS
        "${CMAKE_CURRENT_BINARY_DIR}/greeter_pb2.py"
)
