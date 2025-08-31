import os
import subprocess
import sys

def main():
    print("--- Starting project build automation ---")
    
    # Step 1: Activate the Python virtual environment.
    # This is necessary to ensure Conan is found and used correctly.
    venv_activate_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.venv', 'bin', 'activate')
    print(f"Activating virtual environment from {venv_activate_path}")
    
    # Run the activation script in a new shell.
    # The shell=True and executable='/bin/bash' is required for the 'source' command to work.
    try:
        subprocess.run(f"source {venv_activate_path}", shell=True, executable="/bin/bash", check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error activating virtual environment: {e.output}")
        sys.exit(1)

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
            "conan", "install", ".",
            f"--output-folder={build_dir}",
            "--build=missing",
            f"--profile:build=../{conan_profile_path}",
            f"--profile:host=../{conan_profile_path}"
        ]
        subprocess.run(conan_install_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        print("Conan dependency installation successful.")
    except subprocess.CalledProcessError as e:
        print(f"Error during Conan installation: {e.output}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: 'conan' command not found. Please ensure Conan is installed and in your PATH.")
        sys.exit(1)

    # Step 4: Run the CMake build command.
    print("\n--- Running CMake build ---")
    os.chdir(build_dir)
    try:
        cmake_command = ["cmake", ".."]
        subprocess.run(cmake_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        print("CMake configuration successful.")
    except subprocess.CalledProcessError as e:
        print(f"Error during CMake configuration: {e.output}")
        sys.exit(1)

    try:
        build_command = ["cmake", "--build", "."]
        subprocess.run(build_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        print("C++ build successful.")
    except subprocess.CalledProcessError as e:
        print(f"Error during C++ build: {e.output}")
        sys.exit(1)
    
    print("\n--- Project build complete ---")

if __name__ == "__main__":
    main()
