import os

from cryptography.fernet import Fernet, InvalidToken
import sys

from lib.py.core.paths import res_path


def secure_file(key_path, file_path, encrypt=True, suffix=None):
    """
    :param key_path:
    :param file_path:
    :param encrypt: True for encryption, False for decryption
    :param suffix: If not None, then instead of saving the result in the same file,
                    a new file with suffix added in the name of original file is created.
    :return:
    """
    f = open(key_path, "rb+")
    if f:
        key = f.read()
        # print(key)
        f.close()
    else:
        key = Fernet.generate_key()
        with open(key_path, "wb+") as ff:
            # print(key)
            ff.write(key)

    cipher_suite = Fernet(key)

    new_file_path = file_path
    if suffix:
        file_path_without_ext, file_ext = os.path.splitext(file_path)
        new_file_path = file_path_without_ext + suffix + file_ext
    if encrypt:
        f = open(file_path, 'rb')
        cipher_text = cipher_suite.encrypt(f.read())
        # print(cipher_text)
        f.close()
        ff = open(new_file_path, "wb+")
        ff.write(cipher_text)
        ff.close()
    else:  # decrypt
        # print(str(f.read(), 'utf-8'))
        f = open(file_path, 'rb')
        # plain_text = cipher_suite.decrypt(bytes(f.read(), encoding="utf-8"))
        plain_text = cipher_suite.decrypt(f.read())
        f.close()
        ff = open(new_file_path, "wb+")
        ff.write(plain_text)
        ff.close()


def secure_dir(key_path, dir_path, encrypt, suffix=None):
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            secure_file(key_path, os.path.join(root, file), encrypt, suffix)


def secure(key_path, path, encrypt=True, suffix=None):
    if os.path.isfile(path):
        secure_file(key_path, path, encrypt, suffix)
    else:
        secure_dir(key_path, path, encrypt, suffix)


def unsecure(key_path, path, suffix=None):
    secure(key_path, path, False, suffix)


class TemporarilyUnsecure():
    def __init__(self, file_path, keep=False):
        """
        :param file_path:
        :param keep: Whether to keep the unsecured file or delete it
        """
        self._keep = keep
        self._file_path = file_path
        self._security_key = os.path.join(res_path, "cipher_key")
        self._suffix = "__unsecured"

        fp, ext = os.path.splitext(self._file_path)
        self._unsecure_file_path = fp + self._suffix + ext

    def __enter__(self):
        unsecure(self._security_key, self._file_path, suffix=self._suffix)
        return self._unsecure_file_path

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self._keep:
            os.remove(self._unsecure_file_path)


if __name__ == "__main__":
    dir_py = os.path.dirname(os.path.abspath(__file__))
    dir_lib = os.path.dirname(dir_py)
    dir_root = os.path.dirname(dir_lib)
    cipher_key_path = os.path.join(dir_root, "res/cipher_key")
    target_file = sys.argv[1]

    try:
        if sys.argv[2] == "--decrypt":
            unsecure(cipher_key_path, target_file)
        else:
            secure(cipher_key_path, target_file)
    except IndexError as e:
        secure(cipher_key_path, target_file)
