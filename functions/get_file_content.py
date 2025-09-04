import os
from config import MAX_CHARS

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
