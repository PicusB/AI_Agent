from functions.config import MAX_CHARS
import os
from google.genai import types


def get_file_content(working_directory, file_path):
    try:
        absolute_path_to_wd = os.path.abspath(working_directory)
        absolute_path_to_file = os.path.abspath(os.path.join(working_directory, file_path))
    except:
        return f'Error: Issue creating absolute path to file, check to make sure the input is valid'
    if not absolute_path_to_file.startswith(absolute_path_to_wd):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directroy'
    if not os.path.isfile(absolute_path_to_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(absolute_path_to_file, "r") as f:
            file_content_string = f.read(MAX_CHARS+1)
            if len(file_content_string)>MAX_CHARS:
                file_content_string = file_content_string[:-1]
                file_content_string+=f'[...File "{file_path} truncated at {MAX_CHARS} characters]'
                return file_content_string
            else:
                return file_content_string
    except:
        return f'Error: Error reading the file, ensure the file is valid and the correct type'
    

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and outputs a file's contents to STDOUT",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path for the file to be read.",
            ),
        },
    ),
)
    
    