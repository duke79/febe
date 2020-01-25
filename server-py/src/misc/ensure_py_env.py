import os, sys
from lib.py.core.paths import virtual_env_path, cli_path, python_path, PYTHONPATH

if hasattr(sys, 'real_prefix'):
    print("Exit the current virtual environment %s" % sys.real_prefix)
else:
    if not os.path.exists(python_path):
        cmd = "python3 -m venv %s" % (virtual_env_path)
        os.system(cmd)
