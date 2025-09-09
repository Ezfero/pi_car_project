#!/usr/bin/env python3
import subprocess
import sys
import os
import platform
from pathlib import Path

VENV_COMMANDS = [
    ["{venv_python}", "-m", "pip", "install", "--upgrade", "pip"],
    ["{venv_python}", "-m", "pip", "install", "conan"],
    ["{venv_python}", "-m", "pip", "install", "grpcio", "grpcio-tools"],
]

CUSTOM_PATHS = [
    # LLVM
    "/opt/homebrew/opt/llvm/bin",
    "/usr/local/opt/llvm/bin",
    "/usr/local/llvm/bin",
    "/usr/lib/llvm/bin",
]

def run(command, sudo=False, env=None):
    if sudo:
        command = ["sudo"] + command
    print(f"Running: {' '.join(command)}")
    subprocess.run(command, check=True, env=env)

def install_modules():
    system = platform.system()
    if system == "Linux":
        run(["apt-get", "update"], sudo=True)
        run(["apt-get", "install", "-y", "cmake"], sudo=True)
        run(["apt-get", "install", "-y", "llvm", "clang"], sudo=True)
        run(["apt-get", "install", "-y", "cmake", "ninja-build"], sudo=True)

    elif system == "Darwin":
        run(["brew", "update"])
        run(["brew", "install", "cmake"])
        run(["brew", "install", "llvm"])
        run(["brew", "install", "ninja"])

    else:
        print(f"Unsupported OS: {system}")
        sys.exit(1)

def update_path():
    current_path = os.environ.get("PATH", "")
    path_entries = current_path.split(os.pathsep)

    # Determine shell profile
    shell = os.environ.get("SHELL", "")
    profile_file = None
    if "zsh" in shell:
        profile_file = Path.home() / ".zshrc"
    elif "bash" in shell:
        profile_file = Path.home() / ".bash_profile"

    for candidate in CUSTOM_PATHS:
        candidate_path = Path(candidate)
        if candidate_path.exists() and str(candidate_path) not in path_entries:
            if profile_file:
                with profile_file.open("a") as f:
                    f.write(f'\nexport PATH="{candidate_path}:$PATH"\n')
                print(f"Added {candidate_path} to PATH in {profile_file}")
            else:
                print(f"Please add {candidate_path} to your PATH manually: export PATH={candidate_path}:$PATH")
        elif candidate_path.exists():
            print(f"{candidate_path} already in PATH")
        else:
            print(f"{candidate_path} does not exist, skipping")

def main():
    install_modules()
    update_path()

    venv_dir = ".venv"
    venv_python = os.path.join(venv_dir, "bin", "python")

    if not os.path.exists(venv_dir):
        run([sys.executable, "-m", "venv", venv_dir])
    else:
        print(f"Virtual environment already exists at {venv_dir}")

    for cmd_template in VENV_COMMANDS:
        cmd = [arg.format(venv_python=venv_python) for arg in cmd_template]
        run(cmd)

    print("\n✅ Setup complete! Run conan using:")
    print(f"{venv_python} -m conan install <your_conanfile.py> --profile=linux_armv7 --build=missing")

if __name__ == "__main__":
    main()
