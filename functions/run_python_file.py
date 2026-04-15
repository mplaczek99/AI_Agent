import os
import subprocess

from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    working_path = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Will be True or False
    is_within_working_directory = (
        os.path.commonpath([working_path, target_path]) == working_path
    )

    # Checks if it is outside the working directory
    if not is_within_working_directory:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    # Checks if it is not a file
    if not os.path.isfile(target_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    # Checks if it is not a python file
    if not target_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'

    # Make a subprocess to run the file
    command = ["python", target_path]

    # Adds arguments to the command
    if args is None:
        args = []

    command.extend(args)

    try:
        # Runs the command with subproccesses
        result = subprocess.run(
            command,
            cwd=working_path,
            capture_output=True,
            text=True,
            timeout=30,
        )

        # Build the output string
        parts = []

        # Check the return code
        if result.returncode != 0:
            parts.append(f"Process exited with code {result.returncode}")

        # Checks stdout and stderr of result
        stdout = result.stdout
        stderr = result.stderr

        if not stdout and not stderr:
            parts.append("No output produced")
        else:
            if stdout:
                parts.append(f"STDOUT: {stdout}")
            if stderr:
                parts.append(f"STDERR: {stderr}")

        return "\n".join(parts)

    except subprocess.TimeoutExpired:
        return "Error: Process timed out after 30 seconds"

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns its output (stdout and stderr).",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of arguments to pass to the Python script",
            ),
        },
        required=["file_path"],
    ),
)
