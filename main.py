import os
from dotenv import load_dotenv
import sys
from google import genai
from google.genai import types
from functions.config import SYSTEM_PROMPT
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_files import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function
from functions.run_python_files import run_python_file


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")



client = genai.Client(api_key=api_key)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)


def check_verbosity():
    if len(sys.argv) > 2:
        if sys.argv[2]=="--verbose":
            print("Verbose is ON")
            return True
            
    return False
            
def main():
    if len(sys.argv) < 2:
        print("Error: requires one argument: The string query for the AI")
        sys.exit(1)
    else:
        verbose_toggle = check_verbosity()
        genai_model = "gemini-2.0-flash-001"
        genai_prompt = str(sys.argv[1])
        messages = [types.Content(role="user", parts=[types.Part(text=genai_prompt)])]
        content_response = client.models.generate_content(model = genai_model, 
                                                          contents = messages,
                                                          config = types.GenerateContentConfig(tools =[available_functions],system_instruction = SYSTEM_PROMPT))
    if content_response.function_calls:
        for function_call_part in content_response.function_calls:
            response = call_function(function_call_part, verbose_toggle)
            if not response.parts[0].function_response.response:
                raise Exception("No function response")
            elif verbose_toggle:
                print(f"-> {response.parts[0].function_response.response}")
           
    else:
         print(content_response.text)
        
    if verbose_toggle:
        prompt_tokens = content_response.usage_metadata.prompt_token_count
        response_tokens = content_response.usage_metadata.candidates_token_count
        print(f"\nUser prompt: {genai_prompt}\nPrompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}")

if __name__ == "__main__":
   main()
