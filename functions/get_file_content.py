import os
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    working_path = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Will be True or False
    is_within_working_directory = (
        os.path.commonpath([working_path, target_path]) == working_path
    )

    if not is_within_working_directory:
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    try:
        with open(target_path, "r") as f:
            content = f.read(MAX_CHARS)

            # After reading the first MAX_CHARS...
            if f.read(1):
                content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )

            return content

    except Exception as e:
        return f"Error: {e}"
