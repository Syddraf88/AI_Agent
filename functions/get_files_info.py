import os

from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.abspath(os.path.join(working_directory, directory))
        working_directory_abs = os.path.abspath(working_directory)

        if not os.path.commonpath([full_path, working_directory_abs]) == working_directory_abs:
            return f'Error: Cannot List "{directory}" as it is outside the permitted working directory'
        
        if not os.listdir(full_path):
            return f'Error: "{directory}" is not a directory'
        
        items = os.listdir(full_path)
        result_lines = []

        for item in sorted(items):
            item_path = os.path.join(full_path, item)
            is_dir = os.path.isdir(item_path)
            try:
                file_size = os.path.getsize(item_path)
            except Exception as e:
                file_size = 0
            result_lines.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")
        
        return "\n".join(result_lines)
    
    except Exception as e:
        return f"Error: {e}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)