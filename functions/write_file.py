import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name = "write_file",
    description = "Writes or overwrites text to a file within the permitted working directory.",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "file_path": types.Schema(
                type = types.Type.STRING,
                description = "Path to the file to write/overwrite, relative to the working directory.",
            ),
            "content": types.Schema(
                type = types.Type.STRING,
                description = "Exact content to write to the file.",
            ),
        },
        required = ["file_path", "content"],
    ),
)

def write_file(working_directory, file_path, content):
    target_file_rel = os.path.join(working_directory, file_path)
    target_file_abs = os.path.abspath(target_file_rel)
    working_dir_abs = os.path.abspath(working_directory)

    if not target_file_abs.startswith(working_dir_abs):
        return (f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')

    if not os.path.exists(os.path.dirname(target_file_abs)):
        try:
            os.makedirs(os.path.dirname(target_file_abs))
        except Exception as e:
            return (f'Error creating directory: {e}')
    
    try:
        with open(target_file_abs, "w") as f:
            f.write(content)
        
        return (f'Successfully wrote to "{file_path}" ({len(content)} characters written)')
    
    except Exception as e:
        return (f'Error writing to file: {e}')