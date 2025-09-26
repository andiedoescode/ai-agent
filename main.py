import os
import sys
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.api_core.exceptions import ResourceExhausted
from config import system_prompt, ITER_MAX
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

    # Agent loop - repeatedly ask the model for the next step until it returns a final text or hit ITER_MAX.
    iter_count = 0
    while True:
        iter_count += 1
        if iter_count > ITER_MAX:
            print(f"Max iterations ({ITER_MAX}) reached.")
            sys.exit(1)
        
        # Get the model's next turn w/ optional tool calls. If it returns final text, print and exit.
        try:
            final_response = generate_content(client, gen_model, messages, verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break

        except Exception as e:
            error_str = str(e)

            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                print(f"Rate limited - exhausted your API token quota. Retry again later.")
                break
            else:
                print(f"Error in generate_content: {e}")
                break

# Generating content
def generate_content(client, gen_model, messages, verbose):
    # Call model with entire conversation history (messages) and the tool schemas.
    response = client.models.generate_content(
        model = gen_model, 
        contents = messages,
        config=types.GenerateContentConfig(
            tools = [available_functions],
            system_instruction = system_prompt
        )
    )

    # Extra token info for this turn if --verbose flag used.
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    # Checking over list of response variations (candidates). Add model's message & tool call intents (.content) to conversation history.
    candidates = response.candidates
    for candidate in candidates:
        function_call_content = candidate.content
        messages.append(function_call_content) 

    # If no more tool/function calls this turn, return final response (str).
    if not response.function_calls:
        return response.text
    
    function_responses = []

    # Execute each tool call and capture output.
    for call in response.function_calls:
        # Make a call to the identified tool/function. Returns a function_response part.
        function_call_result = call_function(call, verbose)

        part = function_call_result.parts[0]
        # Checking for existence of function_response in parts, otherwise returns None. Avoids AttributeError.
        fr = getattr(part, "function_response", None)

        # Checking if the structure exists
        if not function_call_result.parts or fr is None:
            raise Exception("Error - :( Empty function call result.")

        if verbose:
            print(f"-> {fr.response}")

        # Collecting tool function responses.
        function_responses.append(part)

    if not function_responses:
        raise Exception("Error - No function responses were generated.")
    
    # Append tool responses as a single user message to conversation history so model can read results next turn.
    new_msg = types.Content(role = "user", parts = function_responses)
    messages.append(new_msg)

if __name__ == "__main__":
    main()
