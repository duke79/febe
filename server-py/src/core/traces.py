from __future__ import print_function

import traceback

import sys
import json as JSON

import os


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def print_exception_traces(e):
    try:
        if os.environ.get("stacktrace"):
            eprint(traceback.format_exc())
        elif sys.argv["stacktrace"]:
            eprint(e)
    except Exception as ee:  # LOL !
        eprint(e)
        pass


def print_for_cli(e, json=False):
    try:
        if os.environ["print_for_cli"]:
            if not json:
                print(e)
            else:
                print(
                    JSON.dumps(e, indent=4, sort_keys=True, default=str))  # https://stackoverflow.com/a/11875813/973425
    except Exception as e:
        # print_exception_traces(e)
        pass


def println(*args, **kwargs):
    """
    Print filename:linenumber + message
    :param args:
    :param kwargs:
    :return:
    """
    from inspect import currentframe, getframeinfo

    # frameinfo = getframeinfo(currentframe())
    # file = str(frameinfo.filename) + ":" + str(frameinfo.lineno)

    from inspect import stack
    caller = getframeinfo(stack()[1][0])
    file = str(caller.filename) + ":" + str(caller.lineno)

    print(file, *args, **kwargs)


class TracePrints(object):
    def __init__(self):
        self.stdout = sys.stdout

    def write(self, s):
        self.stdout.write("Writing %r\n" % s)
        import traceback
        traceback.print_stack(file=self.stdout)

# sys.stdout = TracePrints()
