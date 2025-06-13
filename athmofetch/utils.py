from json import loads


def get_packages(file_path: str, excluded_pkg: list) -> list:
    """Load a JSON file and return its content as a dictionary."""
    with open(file_path, 'r', encoding='utf-8') as file:
        packages = loads(file.read())
    
    return [pkg for pkg in packages if pkg['name'].lower() not in excluded_pkg]


# def download_file(git_path: str, filename)
# https://github.com/Atmosphere-NX/Atmosphere/releases/latest/download/fusee.bin
