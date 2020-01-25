import os, sys
from lib.py.core.paths import python_path, PYTHONPATH, py_path

def main(args):
    cmd = python_path + " " + " ".join(args)
    res = os.system(cmd)
    if res == 256: # in case of failure maybe some dependency is not installed, hence install it
      os.system(python_path + " -m pip install -r " + os.path.join(py_path, "requirements.txt"))
    os.system(cmd)

if __name__ == "__main__":
    main(sys.argv[1:])