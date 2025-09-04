import os

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