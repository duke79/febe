import os

from .traces import println

# user home path
from os.path import expanduser
user_home_path = expanduser("~")

# virtualenv path | python
virtual_env_path = os.path.join(user_home_path, "venv/devas")
if not os.path.exists(virtual_env_path):
    os.makedirs(virtual_env_path)
python_path = os.path.join(virtual_env_path, "bin/python3")

# repo paths
this_file_path = __file__
core_path = os.path.dirname(this_file_path)
py_path = os.path.dirname(core_path)
src_path = os.path.dirname(py_path)
root_path = os.path.dirname(src_path)

alembic_path = os.path.join(py_path, "data/alembic")
lib_path = os.path.dirname(py_path)
batch_path = os.path.join(lib_path, "batch")
react_path = os.path.join(lib_path, "react")
cordova_path = os.path.join(lib_path, "cordova")
res_path = os.path.join(root_path, "res")
projects_path = os.path.join(root_path, "src/projects")

cli_path = os.path.join(py_path, "cli/run.py")
sh_path = os.path.join(src_path, "sh")

# PYTHONPATH
PYTHONPATH = None
if not os.environ["PYTHONPATH"]:
    os.environ["PYTHONPATH"] = root_path
PYTHONPATH = os.environ["PYTHONPATH"]
PYTHONPATH = os.path.abspath(PYTHONPATH)
os.environ["PYTHONPATH"] = PYTHONPATH


class ActiveDir:
    """
    Context manager to work in a specific directory and switch back to original directory once done.
    """

    def __init__(self, dir):
        self._orig_dir = os.path.abspath(os.curdir)
        self._dir = dir

    def __enter__(self):
        println("Switching to dir: " + self._dir)
        os.chdir(self._dir)

    def __exit__(self, exc_type, exc_val, exc_tb):
        println("Switching to dir: " + self._orig_dir)
        os.chdir(self._orig_dir)


def export_all(file_pattern="*.py"):
    from os.path import dirname, basename, isfile
    from inspect import getframeinfo
    from inspect import stack
    caller = getframeinfo(stack()[1][0])
    # file = str(caller.filename) + ":" + str(caller.lineno)
    dir_path = dirname(caller.filename)

    # """Export all files | https://stackoverflow.com/a/1057534/973425"""
    # import glob
    # modules = glob.glob(dir + file_pattern)
    # __all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__.py')]

    # https://stackoverflow.com/questions/2186525/how-to-use-glob-to-find-files-recursively
    modules = list()
    from pathlib import Path

    for filename in Path(dir_path).glob(file_pattern):
        if isfile(filename) and not str(filename).endswith('__.py'):
            modules.append(filename)

    ret = [basename(f)[:-3] for f in modules]
    return ret










import os

# user home path
from os.path import expanduser
user_home_path = expanduser("~")

# virtualenv path | python
virtual_env_path = os.path.join(user_home_path, "venv/vl")
if not os.path.exists(virtual_env_path):
    os.makedirs(virtual_env_path)
python_path = os.path.join(virtual_env_path, "bin/python3")

# repo paths
this_file_path = __file__
core_path = os.path.dirname(this_file_path)
py_path = os.path.dirname(core_path)
src_path = os.path.dirname(py_path)
root_path = os.path.dirname(src_path)

cli_path = os.path.join(py_path, "cli/run.py")
sh_path = os.path.join(src_path, "sh")

# PYTHONPATH
PYTHONPATH = None
if not os.environ["PYTHONPATH"]:
    os.environ["PYTHONPATH"] = root_path
PYTHONPATH = os.environ["PYTHONPATH"]
PYTHONPATH = os.path.abspath(PYTHONPATH)
os.environ["PYTHONPATH"] = PYTHONPATH

class ActiveDir:
    """
    Context manager to work in a specific directory and switch back to original directory once done.
    """

    def __init__(self, dir):
        self._orig_dir = os.path.abspath(os.curdir)
        self._dir = dir

    def __enter__(self):
        print("Switching to dir: " + self._dir)
        os.chdir(self._dir)

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Switching to dir: " + self._orig_dir)
        os.chdir(self._orig_dir)

def ensure_exec_path():
    def ensure_path_in_file(in_path, in_file):
        with open(in_file, "w+") as f:
            for elem in f:
                elem = os.path.abspath(elem)
                if elem == in_path:
                    return
            f.write("\n" + in_path + "\n")

    paths_d_path = "/etc/paths.d/"
    if not os.path.exists(paths_d_path):
        os.makedirs(paths_d_path)
    paths_devas_conf_path = os.path.join(paths_d_path, "devas")
    ensure_path_in_file(sh_path, paths_devas_conf_path)
    