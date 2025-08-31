import os
from pathlib import Path

# Define the project name
project_name = "CarApp"

# Define the project structure
project_structure = {
    ".": [
        "CMakeLists.txt",
        "conanfile.txt",
        "README.md"
    ],
    "cpp_app": [
        "CMakeLists.txt"
    ],
    "cpp_app/src": [
        "main.cpp"
    ],
    "python_app": [
        "pyproject.toml",
        "main.py"
    ],
    "shared_protos": [
        "greeter.proto"
    ]
}

def create_files_and_directories():
    """
    Creates the project directory and the necessary files and subdirectories.
    """
    print(f"Creating project directory '{project_name}'...")
    os.makedirs(project_name, exist_ok=True)
    os.chdir(project_name)

    # Create directories
    for dir_path in project_structure:
        if dir_path != ".":
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            print(f"  - Created directory '{dir_path}'")

    # Create files and populate with initial content
    print("Creating initial project files...")

    # Root CMakeLists.txt
    with open("CMakeLists.txt", "w") as f:
        f.write("""# CMake's minimum required version
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
""")
    print("  - Created CMakeLists.txt")

    # conanfile.txt
    with open("conanfile.txt", "w") as f:
        f.write("""[requires]
catch2/3.4.0
grpc/1.54.3
protobuf/3.21.12

[generators]
CMakeToolchain
CMakeDeps
""")
    print("  - Created conanfile.txt")

    # cpp_app/CMakeLists.txt
    with open("cpp_app/CMakeLists.txt", "w") as f:
        f.write("""# Configure the C++ executable
add_executable(cpp_app_executable src/main.cpp)

# Link to C++ dependencies from Conan and our shared library
target_link_libraries(cpp_app_executable
    PRIVATE
    Catch2::Catch2WithMain
    shared_protos
    gRPC::grpc++
    Protobuf::libprotobuf
)
""")
    print("  - Created cpp_app/CMakeLists.txt")

    # cpp_app/src/main.cpp
    with open("cpp_app/src/main.cpp", "w") as f:
        f.write("""#include <iostream>
#include <memory>
#include <string>

#include <grpcpp/grpcpp.h>
#include "greeter.grpc.pb.h" // Generated header from the .proto file

using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;
using helloworld::Greeter;
using helloworld::HelloReply;
using helloworld::HelloRequest;

class GreeterClient {
public:
    GreeterClient(std::shared_ptr<Channel> channel)
        : stub_(Greeter::NewStub(channel)) {}

    std::string SayHello(const std::string& user) {
        HelloRequest request;
        request.set_name(user);

        HelloReply reply;
        ClientContext context;

        Status status = stub_->SayHello(&context, request, &reply);

        if (status.ok()) {
            return reply.message();
        } else {
            std::cout << "RPC failed: " << status.error_code() << ": " << status.error_message()
                      << std::endl;
            return "RPC failed";
        }
    }

private:
    std::unique_ptr<Greeter::Stub> stub_;
};

int main(int argc, char** argv) {
    std::string target_address = "localhost:50051";
    
    // Create a client and connect to the gRPC server (the Python app)
    GreeterClient client(grpc::CreateChannel(target_address, grpc::InsecureChannelCredentials()));
    
    std::string user = "World from C++";
    std::string reply = client.SayHello(user);
    std::cout << "Client received: " << reply << std::endl;
    
    return 0;
}
""")
    print("  - Created cpp_app/src/main.cpp")

    # python_app/pyproject.toml
    with open("python_app/pyproject.toml", "w") as f:
        f.write("""[tool.poetry]
name = "python_app"
version = "0.1.0"
description = ""
authors = ["Your Name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.9"
grpcio = "^1.54.0"
grpcio-tools = "^1.54.0"
protobuf = "^4.23.4"
requests = "^2.26.0"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
""")
    print("  - Created python_app/pyproject.toml")

    # python_app/main.py
    with open("python_app/main.py", "w") as f:
        f.write("""import grpc
import time
from concurrent import futures

# Import the generated gRPC files
from ..shared_protos import greeter_pb2
from ..shared_protos import greeter_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class GreeterServicer(greeter_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        print(f"Server received: {request.name}")
        return greeter_pb2.HelloReply(message=f"Hello, {request.name}!")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    greeter_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC server started on port 50051. Press Ctrl+C to stop.")
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    print("Hello from the Python App!")
    serve()
""")
    print("  - Created python_app/main.py")

    # shared_protos/greeter.proto
    with open("shared_protos/greeter.proto", "w") as f:
        f.write("""syntax = "proto3";

package helloworld;

// The greeter service definition.
service Greeter {
    // Sends a greeting
    rpc SayHello (HelloRequest) returns (HelloReply) {}
}

// The request message containing the user's name.
message HelloRequest {
    string name = 1;
}

// The response message containing the greetings.
message HelloReply {
    string message = 1;
}
""")
    print("  - Created shared_protos/greeter.proto")

    # README.md
    with open("README.md", "w") as f:
        f.write("# My Polyglot C++ and Python Project\n\nThis project contains both a C++ and a Python application, managed by a unified CMake build system.")
    print("  - Created README.md")

    print(f"\nProject '{project_name}' has been successfully bootstrapped!")
    print(f"You can now navigate into the '{project_name}' directory and start working on your apps.")

if __name__ == "__main__":
    create_files_and_directories()
