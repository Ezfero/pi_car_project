# Configure the C++ executable
# add_executable(core_executable src/main.cpp)

file(GLOB_RECURSE CORE_SOURCES
    src/*.cpp
)

add_executable(core_executable ${CORE_SOURCES})

# Link to C++ dependencies from Conan and our shared library
target_link_libraries(core_executable
    PRIVATE
    apis
    gRPC::grpc++
    protobuf::protobuf
)
