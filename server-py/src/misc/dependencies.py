import os

from lib.py.core.paths import py_path

requirements = os.path.join(py_path, "requirements.txt")


def freeze():
    # cmd = "pipreqs --force " + py_path
    cmd = "python -m pip freeze > " + requirements
    os.system(cmd)


def install():
    os.system("python -m pip install -r " + requirements)


def clean():
    freeze()
    with open(requirements, "r") as f:
        for package in f:
            print("uinstalling module: " + package)
            os.system("python -m pip uninstall -y " + package)
