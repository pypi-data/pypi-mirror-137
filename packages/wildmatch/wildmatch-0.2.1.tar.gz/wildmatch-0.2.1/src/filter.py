"""
Filter input files or stdin lines by a wildmatch filter/config file.
"""

from argparse import ArgumentParser

import sys
import pathlib
import pathspec


def print_error(message: str, exit_code: int = 1) -> None:
    """
    Print an error message to stderr and exit. Helper function to reduce code dup.

    Args:
        message: The message to wrap and print.

    Returns:
        Nothing.
    """
    print(f'ERROR: {message}.' if message[-1] != '.' else f'ERROR: {message}', file=sys.stderr)
    sys.exit(exit_code)


def input_piped(wildfilter: str) -> None:
    """
    Process piped input to this script.

    Args:
        wildfilter: path to the filter file.

    Returns:
        Nothing. The output is printed to stdout.
    """
    with open(wildfilter, encoding='utf-8') as fp_wildfilter:
        spec = pathspec.PathSpec.from_lines('gitwildmatch', fp_wildfilter)
        for path in sys.stdin:
            if not spec.match_file(path):
                print(path, file=sys.stdout, end='')


def input_file(fname: str, wildfilter: str) -> None:
    """
    Process a file, line-by-line.

    Args:
        fname: path to the configuration file to process.
        wildfilter: path to the filter file.

    Returns:
        Nothing. The output is printed to stdout.
    """
    with open(fname, encoding='utf-8') as fp_paths, \
         open(wildfilter, encoding='utf-8') as fp_wildfilter:
        spec = pathspec.PathSpec.from_lines('gitwildmatch', fp_wildfilter)
        for line in fp_paths:
            path = line.rstrip('\n')
            if not spec.match_file(path):
                print(path, file=sys.stdout, end='')


def main() -> None:
    """
    Run argparse.
    """
    parser = ArgumentParser(
        description='Filter lists of paths by arbitrary .gitignore-like configuration files.'
    )

    parser.add_argument('-c', '--conf', type=str, default='.diffignore',
        help='optionally set the configuration file to filter by, defaults to .diffignore'
    )

    parser.add_argument('-i', '--input', type=str, default=None,
        help='optionally specify an input file to filter by the configuration file'
    )

    args = parser.parse_args()

    if not pathlib.Path(args.conf).is_file():
        print_error(f'File {args.conf} does not exist.')

    if not args.input and sys.stdin.isatty():
        print_error('Must provide either an input file for piped values to consume.')
    elif args.input:
        # Read this file's lines, one at a time, for processing.
        input_file(args.input, args.conf)
    else:
        input_piped(args.conf)


if __name__ == '__main__':
    main()
