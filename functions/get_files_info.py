
import os
from google.genai import types


def get_files_info(working_directory, directory = "."):
    print(f"working directory: {working_directory}, directory:{directory}")
    try:
        new_path = os.path.join(working_directory, directory)
        absolute_path = os.path.abspath(new_path)
    except:
        return f"Error: Unable to create absolute path to directory"
    print(f"Listing contents of {absolute_path}:")
    if not absolute_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(absolute_path):
        return f'Error: "{directory}" is not a directory'
    try:
        content_list = os.listdir(absolute_path)
    except:
        return f"Error: unable to create directroy content list"
    return_list = []
    for item in content_list:
        try:
            file_path = os.path.join(absolute_path, item)
            size = os.path.getsize(file_path)
            is_file = os.path.isfile(file_path)
        except:
            return f"Error: Issue creating content list output"
        return_list.append(f"- {item}: file_size={size}, is_dir={not is_file}")
    final_output = "\n".join(return_list)
    print(final_output)
    return final_output

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

if __name__ == "__main__":
    import sys
    import json
    # Parse arguments (assuming correct format, adjust as needed)
    args = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
    result = get_files_info(**args)
    print(result)