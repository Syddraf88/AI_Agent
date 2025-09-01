import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    working_abs = os.path.realpath(working_directory)
    target_abs = os.path.realpath(os.path.join(working_abs, file_path))
    common = os.path.commonpath([working_abs, target_abs])

    if common != working_abs:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(target_abs):
        return f'Error: File "{file_path}" not found.'
    
    if target_abs[-3:] != ".py":
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        commands = ["python3", target_abs]

        if args:
            commands.extend(args)
        
        result = subprocess.run(commands,
                                capture_output=True,
                                text=True,
                                timeout=30,
                                cwd=working_abs, )
        
        output = []

        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        
        return "\n".join(output) if output else "No output produced."
    
    except subprocess.TimeoutExpired:
        return "Error: executing python file: Script timed out."
    
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
    