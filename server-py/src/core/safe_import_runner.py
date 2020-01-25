import os
import sys
from subprocess import Popen, PIPE

last_module = ""

module_ledger = {
    "google.protobuf": "protobuf",
    "libcloud": "apache-libcloud",
    "_cffi_backend": "cffi",
    "geventwebsocket": "gevent-websocket"
}


def decode(arg):
    try:
        return arg.decode("unicode_escape")
    except UnicodeDecodeError as e:
        pass
    return arg


def install(module):
    try:
        module = module_ledger[module]
    except KeyError as e:
        print(e)

    print("Trying to install: " + module)
    cmd = "pip install " + module
    proc = Popen(cmd, stderr=PIPE, stdout=PIPE)
    for line in proc.stdout.readlines():
        line = decode(line)
        print(line)
    for line in proc.stderr.readlines():
        line = decode(line)
        print(line)


def run(cmd):
    global last_module
    proc = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    proc.wait()
    for line in proc.stdout.readlines():
        line = decode(line)
        print(line)
    for line in proc.stderr.readlines():
        line = decode(line)
        if line.__contains__("ModuleNotFoundError: No module named"):
            print(line)
            module = line[38:][:-3]
            if last_module != module:
                last_module = module
                install(module)
                print("Relaunching command: " + cmd)
                run(cmd)
            else:
                print("Unable to install module: " + module)
            break


if __name__ == "__main__":
    cmd = sys.argv[1]
    run(cmd)
