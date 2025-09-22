import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name = "get_files_info",    
    description = "Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "directory": types.Schema(
                type = types.Type.STRING,
                description = "The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    target_dir_rel = os.path.join(working_directory, directory)
    target_dir_abs = os.path.abspath(os.path.join(working_directory, directory))
    working_dir_abs = os.path.abspath(working_directory)
   
    if not target_dir_abs.startswith(working_dir_abs):
        return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    if not os.path.isdir(target_dir_abs):
        return (f'Error: "{directory}" is not a directory')

    try:
        files_info = []
        full_list = list(filter(lambda name: not name.startswith("__"), os.listdir(target_dir_abs)))
        files = sorted(list(filter(
                            lambda name: os.path.isfile(os.path.join(target_dir_rel, name)), full_list)
                        ))
        folders = sorted(list(filter(
                            lambda name: os.path.isdir(os.path.join(target_dir_rel, name)), full_list)
                        ))

        for item in (files + folders):
            file_path = os.path.join(target_dir_rel, item)
            file_size = os.path.getsize(file_path)
            dir_status = os.path.isdir(file_path)
            files_info.append(f"- {item}: file_size={file_size}, is_dir={dir_status}")
        
        return "\n".join(files_info)

    except Exception as e:
        return (f"Error: {e}")