import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv


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
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )
    if verbose == True:
            print(f"User prompt: {user_prompt}")
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()
