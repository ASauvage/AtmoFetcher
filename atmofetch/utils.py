from json import loads


def get_packages(file_path: str, excluded_pkg: list) -> list:
    """Load a JSON file and return its content as a dictionary."""

    if "athmosphere" in map(str.lower, excluded_pkg):
        print(":: Warning: 'Athmosphere' is a reserved package and should not be excluded.")
    if "hekate" in map(str.lower, excluded_pkg):
        print(":: Warning: 'hekate' is a reserved package and should not be excluded.")

    with open(file_path, 'r', encoding='utf-8') as file:
        packages = loads(file.read())
    
    return [pkg for pkg in packages if pkg['name'].lower() not in excluded_pkg]
