import atmofetch
from argparse import ArgumentParser, FileType


if __name__ == "__main__":
    ap = ArgumentParser(prog='athmofetch', description="A simple command-line tool.")
    ap.add_argument('-v', '--version', action='version', version='%(prog)s v' + atmofetch.__version__,
                    help="Show %(prog)s version")
    ap.add_argument('-f', '--package-file', dest="file", default='packages.json',
                    help="Path to the JSON file containing package information. (default: packages.json)")

    sp = ap.add_subparsers(dest='command', required=True)
    
    build_ap = sp.add_parser('build', help="Build an Athmosphere structure folder.")
    build_ap_grp = build_ap.add_mutually_exclusive_group()
    build_ap_grp.add_argument('-e', '--exclude', nargs='*', default=[],
                              help="Exclude homebrews from the build.")
    build_ap_grp.add_argument('-f', '--from-file', dest="from_file", type=FileType('r'),
                              help="Path to a csv file containing homebrews")
    build_ap.add_argument('-V', '--verbose', action='store_true', 
                          help="Enable verbose output.")
    
    fetch_ap = sp.add_parser('fetch', help="Fetch package informations.")
    fetch_ap.add_argument('-e', '--exclude', nargs='*', default=[],
                          help="Exclude packages from the fetch operation.")
    
    list_ap = sp.add_parser('list', help="List available packages.")

    args = ap.parse_args()

    match args.command:
        case 'build':
            if args.from_file:
                args.exclude = atmofetch.get_excluded_packages(args.file, args.from_file.readlines()[0])
            atmofetch.build(args.file, args.exclude, args.verbose)
        case 'fetch':
            atmofetch.fetch(args.file, args.exclude)
        case 'list':
            atmofetch.listpkgs(args.file)
        case _:
            ap.print_usage()
