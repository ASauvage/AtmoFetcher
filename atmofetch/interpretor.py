from os import getcwd, remove, makedirs
from os.path import isfile, isdir
from shutil import move, copy, rmtree
from glob import glob
from zipfile import ZipFile


VARIABLES = dict(
    TMP_DIR=f"{getcwd()}/tmp",
    SD_DIR=f"{getcwd()}/output/SD",
    PAYLOADS_DIR=f"{getcwd()}/output/payloads",
)


class UnknownAction(Exception):
    def __init__(self, action: str):
        super().__init__(f"Unknown action: '{action}'")


class Command:
    """
    <action_key>:<args>

    EXTRACT:<source>,<target>
    MOVE:<source>,<target>
    COPY:<source>,<target>
    MKDIR:<target>
    REMOVE:<source>
    """
    def __init__(self, command: str, verbose: bool = False):
        self.verbose = verbose

        action_key, args = command.split(':')
        args = self._args_formater(args)

        match action_key.upper():
            case 'EXTRACT':
                self._extract(*args)
            case 'MOVE':
                self._move(*args)
            case 'COPY':
                self._copy(*args)
            case 'MKDIR':
                self._mkdir(*args)
            case 'REMOVE':
                self._remove(*args)
            case _:
                raise UnknownAction(action_key)
        
        if self.verbose:
            print(f"└performing action: {action_key} > {','.join(args)}") 


    @staticmethod
    def _args_formater(args: str) -> list[str]:
        args_list = [s.format(**VARIABLES).lstrip(' ') for s in args.split(',')]

        return args_list
    
    def _extract(self, source: str, target: str) -> None:
        with ZipFile(source, 'r') as zip_ref:
            zip_ref.extractall(target)

    def _move(self, source: str, target: str) -> None:
        files = glob(source)
        for file in files:
            move(file, target)

    def _copy(self, source: str, target: str) -> None:
        copy(source, target)

    def _mkdir(self, target: str) -> None:
        makedirs(target, exist_ok=True)

    def _remove(self, source: str) -> None:
        if isfile(source):
            remove(source)

        elif isdir(source):
            rmtree(source)

        else:
            raise FileNotFoundError(source)
