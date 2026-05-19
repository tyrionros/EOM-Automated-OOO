import subprocess
import sys
import os

VENV_DIR = ".venv"

def get_venv_executable(executable_name):
    """
    Returns the path to the executable within the virtual environment.
    Handles differences between Windows and Unix-like systems.
    """
    if os.name == "nt":  # Windows
        return os.path.join(VENV_DIR, "Scripts", f"{executable_name}.exe")
    else:  # Unix-like (macOS, Linux)
        return os.path.join(VENV_DIR, "bin", executable_name)

def setup_venv():
    """
    Creates the virtual environment if it doesn't exist.
    """
    if not os.path.exists(VENV_DIR):
        print(f"Creating virtual environment in {VENV_DIR}...")
        try:
            subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])
            print("Virtual environment created successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error creating virtual environment: {e}")
            sys.exit(1)
    else:
        print("Virtual environment already exists.")

def install_requirements():
    """
    Installs dependencies into the virtual environment.
    """
    requirements_file = "requirements.txt"
    if not os.path.exists(requirements_file):
        print(f"Error: {requirements_file} not found.")
        sys.exit(1)

    venv_pip = get_venv_executable("pip")
    print("Ensuring dependencies are installed in the virtual environment...")
    try:
        subprocess.check_call([venv_pip, "install", "-r", requirements_file])
        print("Requirements checked/installed successfully.\n")
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        sys.exit(1)

def run_main_script():
    """
    Executes the main script in the src directory using the venv python interpreter.
    """
    main_script = os.path.join("src", "main.py")
    venv_python = get_venv_executable("python")

    if os.path.exists(main_script):
        print(f"Running {main_script} using virtual environment...\n")
        try:
            subprocess.check_call([venv_python, main_script])
        except subprocess.CalledProcessError as e:
            print(f"Error running main script: {e}")
            sys.exit(1)
    else:
        print(f"Error: {main_script} not found.")
        sys.exit(1)

if __name__ == "__main__":
    setup_venv()
    install_requirements()
    run_main_script()
