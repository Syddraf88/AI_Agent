import os

def get_file_content(working_directory, file_path):
    abs_working_dis = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory, file_path)) if file_path else abs_working_dis

    if not target_dir.startswith(abs_working_dis):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_dir):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        MAX_CHARS = 10000

        with open(target_dir, "r") as f:
            content = f.read(MAX_CHARS + 1)
            if len(content) > MAX_CHARS:
                new_content = content[:MAX_CHARS] + f'\n[...File "{file_path}" truncated at 10000 characters]'
                #f.seek(0)
                #f.write(new_content)
                #f.truncate()
                return new_content
            else:
                return content
            
    except Exception as e:
        return f"Error: {str(e)}"