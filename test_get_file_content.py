from functions.get_file_content import get_file_content
from config import MAX_CHARS


tests = [
    "lorem.txt",
    "main.py",
    "pkg/calculator.py",
    "/bin/cat",
    "pkg/does_not_exist.py",
]

for test in tests:
    result = get_file_content("calculator", test)
    print(f"\tTest: {test}")

    if result is None:
        print("\tFailed: function returned None\n")
        continue

    if result.startswith("Error:"):
        print(result)
        print()
        continue

    if test == "lorem.txt":
        is_truncated = f"truncated at {MAX_CHARS} characters" in result
        length = len(result)

        print(f"\tLength: {length}")
        print(f"\tLength >= MAX_CHARS: {length >= MAX_CHARS}")
        print(f"\tContains truncation message: {is_truncated}\n")
        continue

    print(result)
    print()
