import os


def get_files_info(working_directory, directory="."):
    try:
        working_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_path, directory))

        # Will be True or False
        is_within_working_directory = (
            os.path.commonpath([working_path, target_path]) == working_path
        )

        if not is_within_working_directory:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_path):
            return f'Error: "{directory}" is not a directory'

        contents = []

        for item in os.listdir(target_path):
            item_path = os.path.join(target_path, item)

            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)

            contents.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(contents)

    except Exception as e:
        return f"Error: {e}"
