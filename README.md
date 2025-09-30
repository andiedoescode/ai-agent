# AI Agent (with Tool Use and Feedback Loop)

This is a Python LLM agent that iteratively calls Gemini with a persistent conversation history, executes tools (file info, read file, run Python, write file), and feeds results back into the loop. It includes error handling, an iteration cap, and a simple CLI for prompts.

## Features
- Conversation message history across iterations
- Tool execution:
    - get_files_info
    - get_file_content
    - run_python_file
    - write_file
- Error handling and termination on final text/response
- Automatic feedback loop until completion or cap
- Simple CLI entry point for prompts

## Quick Start

1. Install depencencies:
    - Python 3.11+
    - uv
2. Set up your Gemini / Google Generative AI API key:
    - Create a .env file in the root folder of this project with: `GEMINI_API_KEY="your_api_key_here"`
3. Run with uv:
    - `uv run main.py "your request here"`

## Project Structure

- main.py -- agent loop and message handling
- config.py -- system and behavior prompt, max character and max iteration variables
- func_calls.py -- Tool model and call function
- functions/ -- tool implementations (with schemas)
- calculator/ -- sample project folder the agent can inspect/run

## How It Works

- Builds a messages list (system/user/model/tool)
- Calls generate_content with the full history
- Appends model candidates to the conversation
- Executes requested tools and appends tool results as messages with user role
- Repeats up to a max iteration count or until response.text (a string) is returned

## Configuration

- API credentials defined in .env
- Model instructions/prompt defined in config.py
- Iteration cap and character cap defined in config.py

## Notes

If using the free tier of the Gemini API, you may run into rate limits and need to wait until the following day to have more tokens. Otherwise, be aware of API costs.