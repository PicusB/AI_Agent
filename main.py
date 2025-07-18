import os
from dotenv import load_dotenv
import sys
from google import genai
from google.genai import types
from functions.config import SYSTEM_PROMPT

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")



client = genai.Client(api_key=api_key)

def check_verbosity():
    if len(sys.argv) > 2:
        if sys.argv[2]=="--verbose":
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
                                                          config = types.GenerateContentConfig(system_instruction = SYSTEM_PROMPT))
        print(content_response.text)
        if verbose_toggle:
            prompt_tokens = content_response.usage_metadata.prompt_token_count
            response_tokens = content_response.usage_metadata.candidates_token_count
            print(f"\nUser prompt: {genai_prompt}\nPrompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}")

if __name__ == "__main__":
    main()
