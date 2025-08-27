import os
from dotenv import load_dotenv
from google import genai
import sys

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    gen_model = "gemini-2.0-flash-001"
    user_args = sys.argv[1:]

    if not user_args:
        print('Prompt error.')
        print('Syntax: python main.py "Your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    user_prompt = " ".join(user_args)

    response = client.models.generate_content(model=gen_model, contents=user_prompt)

    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)
    print(response.text)


if __name__ == "__main__":
    main()
