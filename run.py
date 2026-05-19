import subprocess
import sys
import os

def check_and_install_requirements():
    """
    Checks if requirements are met by trying to import the main dependencies.
    If they are missing, it runs pip install -r requirements.txt.
    """
    requirements_file = "requirements.txt"
    dependencies = ["msal", "requests"]
    
    missing = False
    for dep in dependencies:
        try:
            __import__(dep)
        except ImportError:
            missing = True
            break
            
    if missing:
        if os.path.exists(requirements_file):
            print("Dependencies missing. Installing requirements...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
                print("Requirements installed successfully.\n")
            except subprocess.CalledProcessError as e:
                print(f"Error installing requirements: {e}")
                sys.exit(1)
        else:
            print(f"Error: {requirements_file} not found. Cannot install dependencies.")
            sys.exit(1)
    else:
        print("All dependencies are already met.")

def run_main_script():
    """
    Executes the main script in the src directory.
    """
    main_script = os.path.join("src", "main.py")
    if os.path.exists(main_script):
        print(f"Running {main_script}...\n")
        try:
            # We use subprocess to run the main script to keep the environment clean
            subprocess.check_call([sys.executable, main_script])
        except subprocess.CalledProcessError as e:
            print(f"Error running main script: {e}")
            sys.exit(1)
    else:
        print(f"Error: {main_script} not found.")
        sys.exit(1)

if __name__ == "__main__":
    check_and_install_requirements()
    run_main_script()
