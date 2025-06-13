#
#   /$$$$$$    /$$     /$$                               /$$$$$$$$          /$$               /$$      
#  /$$__  $$  | $$    | $$                              | $$_____/         | $$              | $$      
# | $$  \ $$ /$$$$$$  | $$$$$$$  /$$$$$$/$$$$   /$$$$$$ | $$     /$$$$$$  /$$$$$$    /$$$$$$$| $$$$$$$ 
# | $$$$$$$$|_  $$_/  | $$__  $$| $$_  $$_  $$ /$$__  $$| $$$$$ /$$__  $$|_  $$_/   /$$_____/| $$__  $$
# | $$__  $$  | $$    | $$  \ $$| $$ \ $$ \ $$| $$  \ $$| $$__/| $$$$$$$$  | $$    | $$      | $$  \ $$
# | $$  | $$  | $$ /$$| $$  | $$| $$ | $$ | $$| $$  | $$| $$   | $$_____/  | $$ /$$| $$      | $$  | $$
# | $$  | $$  |  $$$$/| $$  | $$| $$ | $$ | $$|  $$$$$$/| $$   |  $$$$$$$  |  $$$$/|  $$$$$$$| $$  | $$
# |__/  |__/   \___/  |__/  |__/|__/ |__/ |__/ \______/ |__/    \_______/   \___/   \_______/|__/  |__/
#                                                                                       By: @ASauvage                                                                                                     

from requests import get, JSONDecodeError
from .utils import get_packages


MAJOR_VERSION = 1
MINOR_VERSION = 0
__version__ = '.'.join((str(MAJOR_VERSION), str(MINOR_VERSION)))


def build(config: str, exclude: list) -> None:
    """
    Build an Athmosphere structure folder.
    
    :param config: Path to the configuration file.
    :param exclude: List of packages to exclude from the build.
    """
    pkgs = get_packages(config, exclude)

    for pkg in pkgs:
        print(pkg['name'])
    

def fetch(config: str, exclude: list) -> None:
    """
    Build an Athmosphere structure folder.
    
    :param config: Path to the configuration file.
    :param exclude: List of packages to exclude from the build.
    """
    pkgs = get_packages(config, exclude)

    print('╔══════════════════════════════╗',
          '║        LATEST RELEASE        ║',
          '╠═════════════════════╦════════╣', sep="\n")
    for pkg in pkgs:
        try:
            version = get(f"https://api.github.com/repos/{pkg['link']}/releases/latest").json()['tag_name']
        except JSONDecodeError:
            version = "error"
        print(f"║> {pkg['name']:19}║ {version:>6} ║")

    print('╚═════════════════════╩════════╝')