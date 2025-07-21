import os
import subprocess
from google.genai import types
import json

def run_python_file(working_directory, file_path, args=[]):
    
    try:
        absolute_path_to_wd = os.path.abspath(working_directory)            
        absolute_path_to_file = os.path.abspath(os.path.join(working_directory, file_path))
        print(f"Running {absolute_path_to_file} with args:{args}")
    except:
        return f'Error: Issue creating absolute path to file, check to make sure the input is valid'
    if not absolute_path_to_file.startswith(absolute_path_to_wd):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directroy'
    if not os.path.exists(absolute_path_to_file):
        return f'Error: File "{file_path}" not found.'
    if not absolute_path_to_file.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    subprocess_execution_string = ["python3", absolute_path_to_file]
    #REMOVING AS PER BOOTS SUGGESTION TO PASS JSON DATA/DICTIONARY INSTEAD OF VALUES. This makes sense.
    for arg in args:
        subprocess_execution_string.append(arg)
    try:
        response = subprocess.run(subprocess_execution_string,timeout=30, capture_output=True, check=True)
    except subprocess.CalledProcessError as e:
        return f'Process exited with code {e.returncode}'
    stdout_response = response.stdout.decode('utf-8')
    stderr_response = response.stderr.decode('utf-8')
    if stderr_response=="" and stdout_response=="":
        return "No output produced"
    combined_response = "STDOUT: "+stdout_response+"\n"+"STDERR: "+stderr_response
    print(combined_response)
    return combined_response


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes python files within the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path for the python file to be executed.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of arguments to be passed to the script.",
                items = types.Schema(
                    type=types.Type.STRING,
                    description="An argument for the script."
                ),
            ),
        },
        required=["file_path"],
    ),
)