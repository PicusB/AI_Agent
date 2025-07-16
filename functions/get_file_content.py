from config import MAX_CHARS
import os


def get_file_content(working_directory, file_path):
    absolute_path_to_wd = os.path.abspath(working_directory)
    absolute_path_to_file = os.path.abspath(os.path.join(working_directory, file_path))
    if not absolute_path_to_file.startswith(absolute_path_to_wd):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directroy'