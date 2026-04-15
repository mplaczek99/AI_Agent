from google.genai import types
from .get_files_info import schema_get_files_info, get_files_info
from .get_file_content import schema_get_file_content, get_file_content
from .run_python_file import schema_run_python_file, run_python_file
from .write_file import schema_write_file, write_file

available_functions = types.Tool(
    function_declarations=[schema_get_files_info,
                           schema_get_file_content, schema_run_python_file, schema_write_file],
)


def call_function(function_call, verbose=False):
    if verbose:
        # Print something special
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        # Else, just print the function normally
        print(f" - Calling function: {function_call.name}")

    function_map = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    function_name = function_call.name or ""  # Could be None in theory...

    # Checks if functino_name is not in the map
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    # Continues here if valid
    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = "./calculator"

    # Call the function
    try:
        function_result = function_map[function_name](**args)
    except Exception as e:
        print(f"Error: {e}")

    # Returns the Content
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
