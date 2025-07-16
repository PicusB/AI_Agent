
import os

def get_files_info(working_directory, directory = "."):
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
    return final_output