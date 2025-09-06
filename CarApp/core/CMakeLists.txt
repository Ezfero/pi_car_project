cmake_minimum_required(VERSION 4.1)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)


file(GLOB_RECURSE CORE_SOURCES
    src/*.cpp
)

file(GLOB_RECURSE CORE_MODULE_DEFINITIONS
    src/*.ixx
)

add_library(core_modules)
target_sources(core_modules
  PUBLIC
    FILE_SET cxx_modules TYPE CXX_MODULES FILES
    ${CORE_MODULE_DEFINITIONS}
)

# add_library(core_modules
#     # ${CORE_MODULE_DEFINITIONS}
# )



# set(MODULE_SOURCES
#     src/orchestration/ColtrolOrchestrator.ixx
# )

# add_library(ColtrolOrchestratorModule
#     ${MODULE_SOURCES}
# )

add_executable(core_executable ${CORE_SOURCES})


# target_precompile_headers(core_executable PRIVATE ${CORE_MODULE_DEFINITIONS})

# Link to C++ dependencies from Conan and our shared library
target_link_libraries(core_executable
    PRIVATE
    core_modules
    apis
    gRPC::grpc++
    protobuf::protobuf
)
