from json import loads


def get_packages(file_path: str, excluded_pkg: list) -> list:
    """Load a JSON file and return its content as a dictionary."""

    if "atmosphere" in map(str.lower, excluded_pkg):
        print(":: Warning: 'Atmosphere' is a reserved package and should not be excluded.")
    if "hekate" in map(str.lower, excluded_pkg):
        print(":: Warning: 'hekate' is a reserved package and should not be excluded.")

    with open(file_path, 'r', encoding='utf-8') as file:
        packages = loads(file.read())
    
    return [pkg for pkg in packages if pkg['name'].lower() not in excluded_pkg]


def get_excluded_packages(file_path: str, packages_str: str) -> list:
    """Load a JSON file and return its content as a dictionary according to packages."""

    packages_list = [pkg.lstrip(' ') for pkg in packages_str.split(',')]

    if "atmosphere" not in map(str.lower, packages_list):
        print(":: Warning: 'Atmosphere' is a reserved package and should not be excluded.")
    if "hekate" not in map(str.lower, packages_list):
        print(":: Warning: 'hekate' is a reserved package and should not be excluded.")

    with open(file_path, 'r', encoding='utf-8') as file:
        packages = loads(file.read())
    
    return [pkg['name'].lower() for pkg in packages if pkg['name'].lower() not in packages_list]
