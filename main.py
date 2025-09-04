import sys
import os
import time
import random

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
    max_retires = 10
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
    
    for attempt in range(max_retires + 1):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(tools=[available_functions],
                                            system_instruction=system_prompt)
                )
            
            #made_tool_call = False

            #for candidate in (response.candidates or []):
            #    messages.append(candidate.content)

             #   for part in (candidate.content.parts or []):
              #      if part.function_call:
               #         made_tool_call = True
                #        call = part.function_call
                 #       if verbose:
                  #          print(f"- Calling function {call.name}")
                   #     tool_msg = call_function(call, verbose=verbose)
                    #    messages.append(tool_msg)
            # python
            made_tool_call = False

            for cand in (response.candidates or []):
                messages.append(cand.content)  # the model's turn

                fr_parts = []
                for part in (cand.content.parts or []):
                    if part.function_call:
                        made_tool_call = True
                        call = part.function_call
                        if verbose:
                            print(f"- Calling function: {call.name} {call.args}")
                        raw_result = call_function(call, verbose=verbose)

                        payload = raw_result if isinstance(raw_result, dict) else {"result": raw_result}

                        #fr_parts.append(
                            #types.Part.from_function_response(
                                #name=call.name,
                                #response=payload,
                           ##)
                
                if fr_parts:
                    messages.append(types.Content(role="user", parts=fr_parts))

            if verbose == True:
                    print(f"User prompt: {user_prompt}")
                    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
                    print("Response tokens:", response.usage_metadata.candidates_token_count)

            if not made_tool_call and response.text:
                print("Response:")
                print(response.text)
                return response.text

            #else:
                
                #for call in response.function_calls:
                    #if verbose:
                        #print("Model chose:", call.name, call.args)
                    #call_response = call_function(call, verbose=verbose)
                    #messages.append(call_response)
                    #if (
                        #not call_response.parts 
                        #or not call_response.parts[0].function_response
                        #or call_response.parts[0].function_response.response is None
                    #):
                            #raise RuntimeError(f"function response missing: {call_response}")
                    #continue
                    
                    
                if verbose:
                    print(f"-> {call_response.parts[0].function_response.response}")
            
                

        except Exception as e:
            msg = str(e)
            retryable = (
            "429" in msg
            or "RESOURCE_EXHAUSTED" in msg
            or "UNAVAILABLE" in msg
            or "INTERNAL" in msg
            or "DEADLINE_EXCEEDED" in msg
            or "503" in msg
        )
            if attempt == max_retires or not retryable:
                raise   
            delay = 0.5 * (2 ** attempt) + random.uniform(0, 0.2)
            if verbose:
                print(f"Retrying after error ({msg}). Sleeping: {delay:.2f}s...")
            time.sleep(delay)
            continue

    


if __name__ == "__main__":
    main()
