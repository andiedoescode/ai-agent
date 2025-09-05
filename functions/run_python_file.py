import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
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
        arg_list = ["uv", "run", target_file_abs] + args
        result = subprocess.run(
            arg_list, 
            capture_output=True, 
            text=True, 
            timeout=30, 
            cwd=working_dir_abs)

        output = ''

        if result.returncode != 0:
            return (f"Process exited with code {result.returncode}")
        if result.stdout:
            output = f'STDOUT: {result.stdout}'
        if result.stderr:
            output = f'STDERR: {result.stderr}'
        if result.stdout == '':
            output = 'No output produced.'

        return output

    except Exception as e:
        return (f"Error: executing Python file: {e}")