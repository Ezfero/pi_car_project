# CMake's minimum required version
cmake_minimum_required(VERSION 3.25)

if(NOT DEFINED CMAKE_C_COMPILER)
    if(APPLE)
        # Look for Homebrew LLVM on macOS
        find_program(HOMEBREW_LLVM clang HINTS /opt/homebrew/opt/llvm/bin /usr/local/opt/llvm/bin)
        if(HOMEBREW_LLVM)
            message(STATUS "Using LLVM from Homebrew: ${HOMEBREW_LLVM}")
            set(CMAKE_CXX_COMPILER "${HOMEBREW_LLVM}++" CACHE STRING "C++ compiler" FORCE)
        endif()
    elseif(UNIX)
        # On Linux, try clang-21 or clang-22
        find_program(CLANG_BIN clang-21 clang-22 clang)
        if(CLANG_BIN)
            message(STATUS "Using Clang detected on Linux: ${CLANG_BIN}")
            set(CMAKE_CXX_COMPILER "${CLANG_BIN}++" CACHE STRING "C++ compiler" FORCE)
        endif()
    endif()
endif()

# Define the project name
project(CarApp VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_PREFIX_PATH "${CMAKE_PREFIX_PATH};${CMAKE_CURRENT_SOURCE_DIR}/build")


# --- PROTOBUF AND GRPC INTEGRATION ---
find_package(protobuf REQUIRED)
find_package(gRPC CONFIG REQUIRED)

# --- C++ SUB-PROJECT ---
add_subdirectory(core)
add_subdirectory(apis)
add_dependencies(core_executable apis)


# --- PYTHON APPLICATION ---
include(ExternalProject)
ExternalProject_Add(
    platform_wrapper_setup
    SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/platform_wrapper"
    CONFIGURE_COMMAND ""
    BUILD_COMMAND ""
    INSTALL_COMMAND ""
    STEP_TARGETS install_deps
    COMMAND
        ${CMAKE_COMMAND} -E chdir "${CMAKE_CURRENT_SOURCE_DIR}/platform_wrapper"
        poetry install
    # Ensure the python setup runs after the proto files are generated.
    DEPENDS "apis"
)
