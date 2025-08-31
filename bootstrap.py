import os
from pathlib import Path

# Define the project name
project_name = "MyPolyglotApp"

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
""")
    print("  - Created CMakeLists.txt")

    # conanfile.txt
    with open("conanfile.txt", "w") as f:
        f.write("""[requires]
catch2/3.4.0

[generators]
CMakeToolchain
CMakeDeps
""")
    print("  - Created conanfile.txt")

    # cpp_app/CMakeLists.txt
    with open("cpp_app/CMakeLists.txt", "w") as f:
        f.write("""# Configure the C++ executable
add_executable(cpp_app_executable src/main.cpp)

# Link to C++ dependencies from Conan
target_link_libraries(cpp_app_executable PRIVATE Catch2::Catch2WithMain)
""")
    print("  - Created cpp_app/CMakeLists.txt")

    # cpp_app/src/main.cpp
    with open("cpp_app/src/main.cpp", "w") as f:
        f.write("""#include <iostream>

int main() {
    std::cout << "Hello from the C++ App!" << std::endl;
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
requests = "^2.26.0"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
""")
    print("  - Created python_app/pyproject.toml")

    # python_app/main.py
    with open("python_app/main.py", "w") as f:
        f.write("""import requests

def get_joke():
    try:
        response = requests.get("https://official-joke-api.appspot.com/random_joke")
        response.raise_for_status()
        joke_data = response.json()
        print(f"Setup: {joke_data['setup']}")
        print(f"Punchline: {joke_data['punchline']}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching joke: {e}")

if __name__ == "__main__":
    print("Hello from the Python App!")
    get_joke()
""")
    print("  - Created python_app/main.py")

    # README.md
    with open("README.md", "w") as f:
        f.write("# My Polyglot C++ and Python Project\n\nThis project contains both a C++ and a Python application, managed by a unified CMake build system.")
    print("  - Created README.md")

    print(f"\nProject '{project_name}' has been successfully bootstrapped!")
    print(f"You can now navigate into the '{project_name}' directory and start working on your apps.")

if __name__ == "__main__":
    create_files_and_directories()