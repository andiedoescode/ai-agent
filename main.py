import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    gen_model = "gemini-2.0-flash-001"

    # Check for --verbose flag
    verbose = "--verbose" in sys.argv
    user_args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            user_args.append(arg)

    # Error message and exit if script run without input
    if not user_args:
        print('Prompt error.')
        print('Syntax: python main.py "Your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    # Store user prompt and initialize list of messages
    user_prompt = " ".join(user_args)
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    response = client.models.generate_content(
        model=gen_model, 
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt))

    # Extra info if --verbose flag used
    if verbose:
        print("User prompt:", user_prompt)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    
    # Print LLM response
    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()
