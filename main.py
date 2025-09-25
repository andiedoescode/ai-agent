import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt, gen_model
from func_calls import available_functions, available_tools, call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
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

    generate_content(client, messages, verbose)

# Generating content
def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model = gen_model, 
        contents = messages,
        config=types.GenerateContentConfig(
            tools = [available_functions],
            system_instruction = system_prompt
        )
    )

    # Extra info if --verbose flag used
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)


    candidates = response.candidates
    for candidate in candidates:
        function_call_content = candidate.content
        messages.append(function_call_content) 

    if not response.function_calls:
        print("Response:")
        print(response.text)
    
    function_responses = []

    for call in response.function_calls:
        function_call_result = call_function(call, verbose=verbose)

        part = function_call_result.parts[0]
        # Checking for existence of function_response in parts, otherwise returns None. Avoids AttributeError.
        fr = getattr(part, "function_response", None)

        # Checking if the structure exists
        if not function_call_result.parts or fr is None:
            raise Exception(":( Empty function call result.")
            sys.exit(1)

        if verbose:
            print(f"-> {fr.response}")

        function_responses.append(part)


    # candidates = response.candidates
    # made_tool_call = False

    # # For dispatch
    # for cand in candidates:
    #     messages.append(cand.content)

    #     for part in cand.content.parts:
    #         # Check for existence of function_call, otherwise returns None. Avoids AttributeError.
    #         fc = getattr(part, "function_call", None)

    #         # If function_call exists, 
    #         if fc:
    #             made_tool_call = True

    #             func_name = fc.name
    #             func_args = dict(fc.args or {})
    #             func_args.setdefault("working_directory", "calculator")
    #             py_func = available_tools.get(func_name)
            
    #             if not py_func:
    #                 continue

    #             print(f"- Calling function: {func_name}")

    #             result = py_func(**func_args)

    #             fr_part = types.Part(
    #                 function_response = types.FunctionResponse(
    #                     name = func_name,
    #                     id = fc.id,
    #                     response = {"result": result},
    #                 )
    #             )
    #             new_msg = types.Content(role="user", parts=[fr_part])
    #             messages.append(new_msg)

    # if not made_tool_call and response.text:
    #     print("Final response:")
    #     print(response.text)
    #     break
    # else:
    #     continue

    # raise Exception("some sorta error :/")

if __name__ == "__main__":
    main()
