cmake_minimum_required(VERSION 3.25)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)


file(GLOB_RECURSE CORE_SOURCES
    src/*.cpp
)

add_executable(core_executable ${CORE_SOURCES})

# This makes the headers in parallel directores available for inclusion
target_include_directories(core_executable PUBLIC
    ${PROJECT_SOURCE_DIR}/core/src
)

# Link to C++ dependencies from Conan and our shared library
target_link_libraries(core_executable
    PRIVATE
    apis
    gRPC::grpc++
    protobuf::protobuf
)
