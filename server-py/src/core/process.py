from subprocess import Popen, PIPE, CalledProcessError


def execute(cmd, with_type=False):
    """
    :param cmd:
    :param with_type: Yield output type as well
    :return:
    """
    print("cmd: " + cmd)

    cmd = str(cmd).split(" ")

    proc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)

    for line in iter(proc.stderr.readline, ""):
        if len(line) == 0:
            break

        line = line.decode('utf-8')

        if with_type:
            yield {"type": "error", "value": line}
        else:
            yield line

    proc.stderr.close()

    for line in iter(proc.stdout.readline, ""):
        if len(line) == 0:
            break

        line = line.decode('utf-8')

        if with_type:
            yield {"type": "output", "value": line}
        else:
            yield line

    proc.stdout.close()

    return_code = proc.wait()
    if return_code:
        raise Exception(return_code)
