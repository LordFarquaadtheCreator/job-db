def main():
    import subprocess
    import os
    import sys

    DIR_PATH = os.path.dirname(os.path.realpath(__file__))
    AUX_MAIN_PATH = os.path.join(DIR_PATH, "main.py")

    venv_path = os.path.join(DIR_PATH, "env")
    if not os.path.exists(venv_path):
        raise FileNotFoundError("Virtual environment not found at {}".format(venv_path))

    venv_python = os.path.join(venv_path, "bin", "python3")
    if not os.path.exists(venv_python):
        raise FileNotFoundError("Python executable not found at {}".format(venv_python))

    subprocess.check_call([venv_python, AUX_MAIN_PATH, *sys.argv[1:]])


if __name__ == "__main__":
    main()
