from functions.get_files_info import get_files_info


for directory in [".", "pkg", "/bin", "../"]:
    if directory == ".":
        label = "current"
    else:
        label = f"'{directory}'"

    result = get_files_info("calculator", directory)

    print(f"Result for {label} directory:")
    print("\t" + result.replace("\n", "\n\t") + "\n")
