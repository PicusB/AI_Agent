import os
import subprocess

def run_python_files(working_directory, file_path, args=[]):
    print (f'Attmpting to run {file_path}:')
    try:
        absolute_path_to_wd = os.path.abspath(working_directory)            
        absolute_path_to_file = os.path.abspath(os.path.join(working_directory, file_path))
    except:
        return f'Error: Issue creating absolute path to file, check to make sure the input is valid'
    if not absolute_path_to_file.startswith(absolute_path_to_wd):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directroy'
    if not os.path.exists(absolute_path_to_file):
        return f'Error: File "{file_path}" not found.'
    if not absolute_path_to_file.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    subprocess_execution_string = ["python3", absolute_path_to_file]
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
    print(f"STDOUT:\n {stdout_response}")
    print(f"STDERR:\n {stderr_response}")

    return "Process executed successfully!\n ****************** \n"
