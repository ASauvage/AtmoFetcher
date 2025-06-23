r"""
  /$$$$$$    /$$                             /$$$$$$$$          /$$               /$$      
 /$$__  $$  | $$                            | $$_____/         | $$              | $$      
| $$  \ $$ /$$$$$$   /$$$$$$/$$$$   /$$$$$$ | $$     /$$$$$$  /$$$$$$    /$$$$$$$| $$$$$$$ 
| $$$$$$$$|_  $$_/  | $$_  $$_  $$ /$$__  $$| $$$$$ /$$__  $$|_  $$_/   /$$_____/| $$__  $$
| $$__  $$  | $$    | $$ \ $$ \ $$| $$  \ $$| $$__/| $$$$$$$$  | $$    | $$      | $$  \ $$
| $$  | $$  | $$ /$$| $$ | $$ | $$| $$  | $$| $$   | $$_____/  | $$ /$$| $$      | $$  | $$
| $$  | $$  |  $$$$/| $$ | $$ | $$|  $$$$$$/| $$   |  $$$$$$$  |  $$$$/|  $$$$$$$| $$  | $$
|__/  |__/   \___/  |__/ |__/ |__/ \______/ |__/    \_______/   \___/   \_______/|__/  |__/
                                                                                      By: @ASauvage                                                                                                     
"""

from requests import get
from re import match
from os import makedirs, getenv
from .utils import get_packages, get_excluded_packages
from .interpretor import Command


MAJOR_VERSION = 1
MINOR_VERSION = 1
__version__ = '.'.join((str(MAJOR_VERSION), str(MINOR_VERSION)))

GITHUB_API_TOKEN = getenv('GITHUB_API_TOKEN')


def build(config: str, exclude: list = [], verbose: bool = False) -> None:
    """Build an Athmosphere structure folder"""
    print(__doc__)

    print(":: creating folders structure...", end="")
    try:
        makedirs('output/SD/')
        makedirs('output/payloads/')
    except FileExistsError:
        print('fail\nthere is already an output folder, please remove it before running this command.')
        exit(1)
    makedirs('tmp/', exist_ok=True)
    print("Done")

    pkgs = get_packages(file_path=config, excluded_pkg=exclude)
    text_version = "╔═══════════════════════════════════╗\n║         BUILD RELEASES         ║\n╠═════════════════════════╦═════════╣\n"

    for pkg in pkgs:
        print(f":: fetching {pkg['name']}...", end="", flush=True)

        pkg_data = get(f"https://api.github.com/repos/{pkg['link']}/releases/latest", headers={"Authorization": f"Bearer {GITHUB_API_TOKEN}"})
        if not pkg_data.status_code == 200:
            print(f"fail\n    └ {pkg['name']} not founds.")
            continue
        pkg_data = pkg_data.json()
        
        text_version += f"║> {pkg['name']:23}║ {pkg_data['tag_name']:>7} ║\n"
        for file in pkg['desiredFiles']:
            if verbose:
                print(f"\n    └fetching '{file['filename']}'...", end="", flush=True)
            link = ""

            for asset in pkg_data['assets']:
                if match(file['patern'], asset['name']):
                    link = asset['browser_download_url']
                    break

            if not link:
                print(f"{'fail' if verbose else ''}\n    └ unable to found {file['filename']} in assets")
                continue

            dfile = get(link)

            with open(f'tmp/{file['filename']}', 'wb') as f:
                f.write(dfile.content)
            if verbose:
                print(f"done")

            for action in file['actions']:
                Command(command=action, verbose=verbose)
                
        print("done")
    
    print(":: writing README output...", end="", flush=True)
    with open('output/README.txt', 'w', encoding='utf-8') as f:
        f.write("This build was created using atmofetch.\n")
        f.write(text_version + "╚═════════════════════════╩═════════╝")
    print("done\n:: deleting tmp folder...", end="", flush=True)

    Command("REMOVE:{TMP_DIR}")

    print("done",
          ":: build complete!\n",
          "You can now copy the 'output/SD' folder to your SD card.", sep="\n")
    

def fetch(config: str, exclude: list) -> None:
    """Build an Athmosphere structure folder"""

    pkgs = get_packages(file_path=config, excluded_pkg=exclude)

    print('╔════════════════════════════════╗',
          '║         LATEST RELEASE         ║',
          '╠═══════════════════════╦════════╣', sep="\n")
    for pkg in pkgs:
        try:
            version = get(f"https://api.github.com/repos/{pkg['link']}/releases/latest").json()['tag_name']
        except KeyError:
            version = "error"
        print(f"║> {pkg['name']:21}║ {version:>6} ║")

    print('╚═══════════════════════╩════════╝')


def listpkgs(config: str) -> None:
    """List available packages"""
    pkgs = [pkg['name'] for pkg in get_packages(config, [])]
    
    print(', '.join(pkgs))
