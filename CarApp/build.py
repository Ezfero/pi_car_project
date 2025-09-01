import os
import subprocess
import sys

def main():
    """
    Main function to automate the Conan and CMake build process.
    """
    print("--- Starting project build automation ---")

    # Step 1: Set paths to executables within the virtual environment.
    venv_bin_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.venv', 'bin')
    conan_path = os.path.join(venv_bin_path, 'conan')
    cmake_path = "cmake"
    # cmake_path = os.path.join(venv_bin_path, 'cmake')

    # if not os.path.exists(conan_path) or not os.path.exists(cmake_path):
    #     print("Error: Conan or CMake executable not found in virtual environment.")
    #     print("Please run 'python3 setup_env.py' first to set up the environment.")
    #     sys.exit(1)
        
    # Step 2: Create the build directory if it doesn't exist.
    build_dir = "build"
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)
        print(f"Created directory: {build_dir}")

    # Step 3: Use Conan to install dependencies and generate toolchain file.
    print("\n--- Installing Conan dependencies ---")
    
    # Determine the correct Conan profile based on the platform.
    if sys.platform == 'darwin':
        conan_profile_path = "conan/macos.profile"
    elif "linux" in sys.platform:
        conan_profile_path = "conan/raspberry.profile"
    else:
        print("Error: Unsupported platform detected.")
        sys.exit(1)

    try:
        conan_install_command = [
            conan_path, "install", ".",
            f"--output-folder={build_dir}",
            "--build=missing",
            f"--profile:build={conan_profile_path}",
            f"--profile:host={conan_profile_path}"
        ]
        subprocess.run(conan_install_command, check=True, text=True)
        print("Conan dependency installation successful.")
    except subprocess.CalledProcessError as e:
        print(f"Error during Conan installation: {e.output}")
        sys.exit(1)

    # Step 4: Run the CMake build command.
    print("\n--- Running CMake build ---")
    # os.chdir(build_dir)
    try:
        cmake_command = [cmake_path, ".", 
                         f"-DCMAKE_TOOLCHAIN_FILE={build_dir}/conan_toolchain.cmake",
                         f"-DCMAKE_PREFIX_PATH={build_dir}",
                         "-DCMAKE_BUILD_TYPE=Release"]
        subprocess.run(cmake_command, check=True, text=True)
        print("CMake configuration successful.")
    except subprocess.CalledProcessError as e:
        print(f"Error during CMake configuration: {e.output}")
        sys.exit(1)

    try:
        build_command = [cmake_path, "--build", "."]
        subprocess.run(build_command, check=True, text=True)
        print("C++ build successful.")
    except subprocess.CalledProcessError as e:
        print(f"Error during C++ build: {e.output}")
        sys.exit(1)
    
    print("\n--- Project build complete ---")

if __name__ == "__main__":
    main()
