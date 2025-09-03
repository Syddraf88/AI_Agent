import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

from call_function import call_function
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python import schema_run_python_file

available_functions = types.Tool(function_declarations=[
     schema_get_files_info,
     schema_get_file_content,
     schema_write_file,
     schema_run_python_file
])

def main():
    load_dotenv()

    args = sys.argv
    verbose = False
    prompt = []
   

    if len(args) < 2:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)
    
    for arg in args[1:]:
        if arg != "--verbose":
            prompt.append(arg)
        elif arg == "--verbose":
            verbose = True
   
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(prompt)

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]

    generate_content(client, messages, verbose, user_prompt)

def generate_content(client, messages, verbose, user_prompt):
    try_count = 10
    reply = "I'M JUST A ROBOT"
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    try:
        while try_count > 0:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(tools=[available_functions],
                                            system_instruction=system_prompt)
                )
            
        if response.candidates:
             for candidate in response.candidates:
                  messages.append(candidate.content)

        if verbose == True:
                print(f"User prompt: {user_prompt}")
                print("Prompt tokens:", response.usage_metadata.prompt_token_count)
                print("Response tokens:", response.usage_metadata.candidates_token_count)

        if not response.function_calls:
            print("Response:")
            print(response.text)

        else:
            
            for call in response.function_calls:
                if verbose:
                    print("Model chose:", call.name, call.args)
                call_response = call_function(call, verbose=verbose)
                messages.append(call_response)
                if (
                    not call_response.parts 
                    or not call_response.parts[0].function_response
                    or call_response.parts[0].function_response.response is None
                ):
                        raise RuntimeError(f"function response missing: {call_response}")
                
                
            if verbose:
                print(f"-> {call_response.parts[0].function_response.response}")
        
        try_count -= 1

    except Exception as e:
         print(f"Exception: {e}")
    


if __name__ == "__main__":
    main()
