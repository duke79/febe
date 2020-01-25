import errno
import os
import shutil

from lib.py.core.paths import ActiveDir, root_path


def forget_in_history(file_path):
    """
    Remove the file from git history and create a new stub in place of the file.
    :param file_path:
    :return:
    """
    cmd_args = {'file_path': file_path}
    cmd_remove_file = '''
    git filter-branch -f --index-filter "git rm -rf --cached --ignore-unmatch {file_path}" HEAD
    '''.format_map(cmd_args)
    print("\nReplacing %s" % file_path)
    print(cmd_remove_file)
    os.system(cmd_remove_file)
    if not os.path.exists(file_path):
        try:
            os.makedirs(os.path.dirname(file_path))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    open(file_path, 'a').close()
    cmd_add_to_git = "git add %s -f" % file_path
    os.system(cmd_add_to_git)
    cmd_commit = 'git commit -a -m "removed \'%s\' from git history"' % file_path
    os.system(cmd_commit)
    pass


def forget(file_path):
    """
    Stop tracking this file.
    :param file_path:
    :return:
    """
    os.system("git rm --cached " + file_path)


def stats(repo=None):
    """
    :param repo: Repo to clone for stats
    :return:
    """
    repo_path = root_path

    if repo is not None:
        repo_path = os.path.normpath("temprepo")
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path, ignore_errors=False, onerror=None)
        cmd = "git clone %s %s" % (repo, repo_path)
        os.system(cmd)

    with ActiveDir(repo_path):
        cmd = "git-quick-stats"
        os.system(cmd)


if __name__ == "__main__":
    # Take file/folder path as input
    path_to_file = input("path_to_file:\t")

    # If folder, recursively traverse all files and remove it from history
    if os.path.isdir(path_to_file):
        for r, d, f in os.walk(path_to_file):
            for file in f:
                forget_in_history(str(os.path.join(r, file)).replace('\\', '/'))
    else:  # If folder, simply remove it from history
        forget_in_history(path_to_file.replace('\\', '/'))
