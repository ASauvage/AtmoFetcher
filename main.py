import atmofetch
from argparse import ArgumentParser


if __name__ == "__main__":
    ap = ArgumentParser(prog='athmofetch', description="A simple command-line tool.")
    ap.add_argument('-v', '--version', action='version', version='%(prog)s v' + atmofetch.__version__,
                    help="Show %(prog)s version")
    ap.add_argument('-V', '--verbose', action='store_true',
                    help="Enable verbose output.")
    ap.add_argument('-f', '--file', default='packages.json',
                    help="Path to the JSON file containing package information.")

    sp = ap.add_subparsers(dest='command', required=True, help="Available commands.")
    
    build_ap = sp.add_parser('build', help="Build an Athmosphere structure folder.")
    build_ap.add_argument('-e', '--exclude', nargs='*', default=[],
                          help="Exclude packages from the build.")
    build_ap.add_argument('-T', '--no-textfile', action='store_true',
                          help="Avoid generating a versioning textfile.")
    build_ap.add_argument('-O', '--overwrite', action='store_true',
                          help="Overwrite the output folder if it exists.")
    
    fetch_ap = sp.add_parser('fetch', help="Fetch package information.")
    fetch_ap.add_argument('-e', '--exclude', nargs='*', default=[],
                          help="Exclude packages from the fetch operation.")
    
    list_ap = sp.add_parser('list', help="List available packages.")


    args = ap.parse_args()

    match args.command:
        case 'build':
            atmofetch.build(args.file, args.exclude, args.overwrite, args.verbose)
        case 'fetch':
            atmofetch.fetch(args.file, args.exclude)
        case 'list':
            atmofetch.listpkgs(args.file)
        case _:
            ap.print_usage()
