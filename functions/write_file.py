import os
from google.genai import types

#Writes the content to a working_directory\file_path and creates the file if it does not exist.

def write_file(working_directory, file_path, content):
    try:
        absolute_path_to_wd = os.path.abspath(working_directory)
        absolute_path_to_file = os.path.abspath(os.path.join(working_directory, file_path))
    except:
        return f'Error: Issue creating absolute path to file, check to make sure the input is valid'
    if not absolute_path_to_file.startswith(absolute_path_to_wd):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directroy'
    #if not absolute_path_to_file.endswith(".txt"):
    #    return f'Please specify a .txt file to write to'
    try:
        directory_path = os.path.dirname(absolute_path_to_file)
    except:
        return f'Error validating directory for {absolute_path_to_file}'
    if not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path)
        except:
            return f'Error: uanble to create path: {directory_path}'
    try:
        with open(absolute_path_to_file, "w") as f:
            f.write(content)
    except Exception as e:
        return f'Error: Unable to write content to {file_path}. {e}'
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to the specified file, overwriting any existing contents",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path for the file to be written to.",
            ),
             "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)