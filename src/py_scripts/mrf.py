import argparse


def generate_command():
    # Create the argument parser
    parser = argparse.ArgumentParser(
        description='Generate shell command for finding modified files.'
    )

    # Add arguments to the parser
    parser.add_argument(
        '-p',
        '--path',
        default='$(pwd)',
        help='Starting path for the find command, default to the current working directory.',
    )
    parser.add_argument(
        '-mid',
        '--mindepth',
        type=int,
        default=1,
        help='Minimum depth for the find command.',
    )
    parser.add_argument(
        '-mxd',
        '--maxdepth',
        type=int,
        default=5,
        help='Maximum depth for the find command.',
    )
    parser.add_argument(
        '-c', '--count', type=int, default=5, help='Number of files to display.'
    )
    parser.add_argument(
        '-n',
        '--name',
        type=str,
        default='',
        help='Optional regex pattern to match the file names. If supplied, only files with names matching the pattern will be listed.',
    )

    # Parse the arguments
    args = parser.parse_args()

    # Construct the find command string conditionally including name matching
    name_match_part = f"-name '{args.name}'" if args.name else ''
    command = (
        f'find "{args.path}" -mindepth {args.mindepth} -maxdepth {args.maxdepth} {name_match_part} -type f '
        f'-exec stat --format=\'%y %n\' {{}} + | sort | tail -n {args.count}'
    )

    # Print the command
    print(command)


if __name__ == "__main__":
    generate_command()
