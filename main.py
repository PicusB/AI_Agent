import os
from dotenv import load_dotenv
import sys
from google import genai
from google.genai import types
from functions.config import SYSTEM_PROMPT
from functions.config import MAX_AI_LOOPS
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
    
    verbose_toggle = check_verbosity()
    genai_model = "gemini-2.0-flash-001"
    genai_prompt = str(sys.argv[1])
    messages = [types.Content(role="user", parts=[types.Part(text=genai_prompt)])]
    current_ai_loops = 0    
    
    #content_response = client.models.generate_content(model = genai_model,
    #                                                      contents=messages,
    #                                                      config = types.GenerateContentConfig(tools = [available_functions], system_instruction=SYSTEM_PROMPT))

    while current_ai_loops<MAX_AI_LOOPS:
        try:
            content_response = client.models.generate_content(model = genai_model,
                                                          contents=messages,
                                                          config = types.GenerateContentConfig(tools = [available_functions], system_instruction=SYSTEM_PROMPT))
        except Exception as e:
            print(f"Issue creating new content_response: {e}")    
            break

        if not content_response.function_calls:
            if content_response.text:
                break 

        try:
            if content_response.candidates:
                for candidate in content_response.candidates:
                    messages.append(candidate.content)
        except Exception as e:
            print(f"Issue with checking candidates: {e}")
            break

        try:
            if content_response.function_calls:
                for function_call_part in content_response.function_calls:
                    response = call_function(function_call_part, verbose_toggle)
                    if not response.parts[0].function_response.response:
                        raise Exception("No function response")
                    elif verbose_toggle:
                        print(f"-> {response.parts[0].function_response.response}")
                    #appends the response to the function call (type=types.Content)
                    messages.append(response)
        except Exception as e:
            print(f"issue with running fucntions: {e}")
            break

        current_ai_loops+=1


    
    if content_response.text:
        print(f'response: {content_response.text}, exited after {current_ai_loops} loops')
    else:
        print(f'Maximum number of tries ({MAX_AI_LOOPS}) reached with no conclusive response')
        
    if verbose_toggle:
        prompt_tokens = content_response.usage_metadata.prompt_token_count
        response_tokens = content_response.usage_metadata.candidates_token_count
        print(f"\nUser prompt: {genai_prompt}\nPrompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}")

if __name__ == "__main__":
   main()
