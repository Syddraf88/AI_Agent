import os
from google.genai import types
def write_file(working_directory, file_path, content):
    working_abs = os.path.realpath(working_directory)
    target_abs = os.path.realpath(os.path.join(working_abs, file_path))
    common = os.path.commonpath([working_abs, target_abs])
    
    if common != working_abs:
        return f"Error: Cannot write to file path  '{file_path}' is outside working directory"

    try:
        parent_dir = os.path.dirname(target_abs)
        os.makedirs(parent_dir, exist_ok=True)

        with open(target_abs, "w") as f:
                f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to the file specified with the constraint that the file must be within working_directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file into which to write.",
            ),
            "content": types.Schema(
                 type=types.Type.STRING,
                 description="The content to write to the file."
            )
        },
    ),
)