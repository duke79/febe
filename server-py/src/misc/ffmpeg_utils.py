import os


def convert_mkv_to_mp4(file_path):
    pre, ext = os.path.splitext(os.path.normpath(file_path))
    if ext in (".mkv", ".avi", ".flv", ".wmv", ".mov"):
        target_path = pre + ".mp4"
        # https://gist.github.com/jamesmacwhite/58aebfe4a82bb8d645a797a1ba975132
        cmd_mkv_to_mp4_args = {
            "source_file_path": os.path.normpath(file_path),
            "target_file_path": os.path.normpath(target_path)
        }
        cmd_mkv_to_mp4 = '''ffmpeg -i "{source_file_path}" -c copy "{target_file_path}" '''.format_map(cmd_mkv_to_mp4_args)
        print(cmd_mkv_to_mp4)
        os.system(cmd_mkv_to_mp4)


if __name__ == "__main__":
    # Take file/folder path as input
    path_to_file = input("path_to_file:\t")

    # If folder, recursively traverse all files and convert it
    if os.path.isdir(path_to_file):
        for r, d, f in os.walk(path_to_file):
            for file in f:
                convert_mkv_to_mp4(str(os.path.join(r, file)).replace('\\', '/'))
    else:  # If folder, simply convert it
        convert_mkv_to_mp4(path_to_file.replace('\\', '/'))
