import os

from google.genai import types


def write_file(working_directory, file_path, content):
    working_path = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Will be True or False
    is_within_working_directory = (
        os.path.commonpath([working_path, target_path]) == working_path
    )

    if not is_within_working_directory:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if os.path.isdir(target_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    try:
        # Create parent dirts if needed
        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        # Open the file in write mode
        with open(target_path, "w") as f:
            # Replace its contents with content
            f.write(content)

        return (
            f'Successfully wrote to "{
                file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=(
        "Writes content to a file within the working directory. "
        "Creates the file if it does not exist, or overwrites it if it does."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write into the file",
            ),
        },
        required=["file_path", "content"],
    ),
)
