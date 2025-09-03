#!/usr/bin/env python3
import subprocess
import sys
import os
import platform

VENV_COMMANDS = [
    ["{venv_python}", "-m", "pip", "install", "--upgrade", "pip"],
    ["{venv_python}", "-m", "pip", "install", "conan"],
    ["{venv_python}", "-m", "pip", "install", "grpcio", "grpcio-tools"],
]

def run(command, sudo=False, env=None):
    if sudo:
        command = ["sudo"] + command
    print(f"Running: {' '.join(command)}")
    subprocess.run(command, check=True, env=env)

def install_cmake():
    system = platform.system()
    if system == "Linux":
        run(["apt-get", "update"], sudo=True)
        run(["apt-get", "install", "-y", "cmake"], sudo=True)
    elif system == "Darwin":
        run(["brew", "update"])
        run(["brew", "install", "cmake"])
    else:
        print(f"Unsupported OS: {system}")
        sys.exit(1)

def main():
    install_cmake()

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
