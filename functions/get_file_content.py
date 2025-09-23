import os
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name = "get_file_content",
    description = f"Reads and returns the first {MAX_CHARS} characters of the content from a specified file within the working directory.",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "file_path": types.Schema(
                type = types.Type.STRING,
                description = "Relative path to the file to read.",
            ),
        },
        required = ["file_path"],
    ),
)

def get_file_content(working_directory, file_path):
    target_file_rel = os.path.join(working_directory, file_path)
    target_file_abs = os.path.abspath(target_file_rel)
    working_dir_abs = os.path.abspath(working_directory)

    if not target_file_abs.startswith(working_dir_abs):
        return (f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
    
    if not os.path.isfile(target_file_abs):
        return (f'Error: File not found or is not a regular file: "{file_path}"')

    try:
        with open(target_file_abs, "r") as f:
            file_content = f.read(MAX_CHARS)
            if os.path.getsize(target_file_abs) > MAX_CHARS:
                return file_content + f'[...File "{file_path}" truncated at 10000 characters]'
            return file_content
        
    except Exception as e:
        return (f'Error: {e}')
