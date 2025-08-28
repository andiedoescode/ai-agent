import os

def get_files_info(working_directory, directory="."):
    relative_path = os.path.join(working_directory, directory)
    absolute_path = os.path.abspath(os.path.join(working_directory, directory))

    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory, directory))
   
    if working_dir_abs not in target_dir:
        return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    if not os.path.isdir(target_dir):
        return (f'Error: "{directory}" is not a directory')

    try:
        files_info = []
        full_list = list(filter(lambda name: not name.startswith("__"), os.listdir(target_dir)))
        files = sorted(list(filter(
                            lambda name: os.path.isfile(os.path.join(relative_path, name)), full_list)
                        ))
        folders = sorted(list(filter(
                            lambda name: os.path.isdir(os.path.join(relative_path, name)), full_list)
                        ))

        for item in (files + folders):
            file_path = os.path.join(relative_path, item)
            file_size = os.path.getsize(file_path)
            dir_status = os.path.isdir(file_path)
            files_info.append(f"- {item}: file_size={file_size}, is_dir={dir_status}")
        
        return "\n".join(files_info)

    except Exception as e:
        print(f"Error: {e}")