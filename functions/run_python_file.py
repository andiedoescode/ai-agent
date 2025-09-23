import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name = "run_python_file",
    description = "Executes a Python file within the specified working directory and returns the output from the interpreter.",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "file_path": types.Schema(
                type = types.Type.STRING,
                description = "Relative path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type = types.Type.ARRAY,
                items = types.Schema(
                    type = types.Type.STRING,
                    description = "Optional arguments to pass into the Python file.",
                ),
                description = "Optional arguments to pass into the Python file."
            ),
        },
        required = ["file_path"],
    ),
)

def run_python_file(working_directory, file_path, args=None):

    target_file_rel = os.path.join(working_directory, file_path)
    target_file_abs = os.path.abspath(target_file_rel)
    working_dir_abs = os.path.abspath(working_directory)
    
    if not target_file_abs.startswith(working_dir_abs):
        return (f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')

    if not os.path.exists(target_file_abs):
        return (f'Error: File "{file_path}" not found.')
    
    if not file_path.endswith(".py"):
        return (f'Error: "{file_path}" is not a Python file.')
    
    try:
        arg_list = ["uv", "run", target_file_abs]
        if args:
            arg_list.extend(args)
        # if args=[] in the func dec, then:
        # arg_list = ["uv", "run", target_file_abs, *args]
        result = subprocess.run(
            arg_list, 
            capture_output=True, 
            text=True, 
            timeout=30, 
            cwd=working_dir_abs)

        if result.returncode != 0:
            return (f"Process exited with code {result.returncode}")
        if result.stdout:
            return (f'STDOUT: {result.stdout}')
        if result.stderr:
            return (f'STDERR: {result.stderr}')
        if result.stdout == '':
            return ('No output produced.')

    except Exception as e:
        return (f"Error: executing Python file: {e}")