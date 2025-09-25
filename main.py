import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt
from func_calls import available_functions, available_tools, call_function

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

    # Generating content
    response = client.models.generate_content(
        model = gen_model, 
        contents = messages,
        config=types.GenerateContentConfig(
            tools = [available_functions],
            system_instruction = system_prompt
        )
    )

    candidates = response.candidates
    for cand in candidates:
        messages.append(cand.content)

        for part in cand.content.parts:
            fc = getattr(part, "function_call", None)

            if fc:
                func_name = fc.name
                func_args = fc.args
                func_args.setdefault("working_directory", ".")
                py_func = available_tools.get(func_name)
                result = py_func(**func_args)

                fr_part = types.Part(
                    function_response = types.FunctionResponse(
                        name = func_name,
                        id = fc.id,
                        response = {"result": result},
                    )
                )
                new_msg = types.Content(role="user", parts=[fr_part])
                messages.append(new_msg)

    # Extra info if --verbose flag used
    if verbose:
        print("User prompt:", user_prompt)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    
    # Print LLM response
    if response.function_calls:
        for call in response.function_calls:
            function_call_result = call_function(call, verbose=verbose)

            # Checking if the structure exists
            if not function_call_result.parts:
                print("ERROR: No response found.")
                sys.exit(1)
            
            part = function_call_result.parts[0]

            # Checking for existence of part.function_response, otherwise returns None. Avoids AttributeError.
            fr = getattr(part, "function_response", None)
            if fr is None or fr.response is None:
                print("ERROR: No response found.")
                sys.exit(1)

            if verbose:
                print(f"-> {fr.response}")

    else:
        print("Response:")
        print(response.text)

if __name__ == "__main__":
    main()
