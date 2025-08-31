# CMake's minimum required version
cmake_minimum_required(VERSION 3.15)

# Define the project name
project(MyPolyglotApp VERSION 1.0.0 LANGUAGES CXX)

# --- CONAN INTEGRATION (C++ DEPENDENCIES) ---
# Find Conan and configure a new install folder.
# This ensures that Conan's generated files are separate from the build.
find_package(Conan REQUIRED)
conan_cmake_configure(
    REQUIRES
        catch2/3.4.0
    GENERATORS
        CMakeToolchain
        CMakeDeps
    BUILD
        missing
)

# --- C++ SUB-PROJECT ---
# Add the C++ application subdirectory.
# The CMakeLists.txt inside this folder will handle its specific build.
add_subdirectory(cpp_app)

# --- PYTHON APPLICATION ---
# Use CMake's ExternalProject to manage the Python app.
# This tells CMake to run a separate build process for the Python part.
# This assumes you have Poetry installed on your system.
include(ExternalProject)
ExternalProject_Add(
    python_app_setup
    SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/python_app"
    CONFIGURE_COMMAND ""
    BUILD_COMMAND ""
    INSTALL_COMMAND ""
    # Define a custom step to install Python dependencies.
    # The --with poetry part is crucial for making the build system use the right tool.
    # This also creates a virtual environment for the Python app.
    STEP_TARGETS install_deps
    COMMAND
        ${CMAKE_COMMAND} -E chdir "${CMAKE_CURRENT_SOURCE_DIR}/python_app"
        poetry install
)

# --- OPTIONAL: LINKING THE TWO APPS ---
# If your C++ app needs to interact with the Python app (e.g., call a script)
# you can define a dependency here.
# This ensures the Python setup runs before the C++ build.
add_dependencies(cpp_app_executable python_app_setup)
