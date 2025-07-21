
from google.genai import types
from functions.run_python_files import run_python_file
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file


def call_function(function_call_part, verbose = False):
    function_name = function_call_part.name
    function_args = function_call_part.args
    working_dir = "./calculator"
    function_args["working_directory"]=working_dir
    
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")
    match function_name:
        case "get_file_content":
            function_result = get_file_content(**function_args)
        case "write_file":
            function_result = write_file(**function_args)
        case "get_files_info":
            #can do it this way but have to convert the dictionary values, check the main block from get_files_info
            function_result = get_files_info(**function_args)
        case "run_python_file":
            function_result = run_python_file(**function_args)
        case _:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function: {function_name}"},
                    )
                ],
            )
    #print(f'function_result: {function_result}')
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )


            
