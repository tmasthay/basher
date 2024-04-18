import argparse


def generate_command():
    # Create the argument parser
    parser = argparse.ArgumentParser(
        description='Generate shell command for finding modified files.'
    )

    # Add arguments to the parser
    parser.add_argument(
        '--path',
        default='$(pwd)',
        help='Starting path for the find command, default to the current working directory.',
    )
    parser.add_argument(
        '--mindepth',
        type=int,
        default=1,
        help='Minimum depth for the find command.',
    )
    parser.add_argument(
        '--maxdepth',
        type=int,
        default=5,
        help='Maximum depth for the find command.',
    )
    parser.add_argument(
        '--count', type=int, default=5, help='Number of files to display.'
    )

    # Parse the arguments
    args = parser.parse_args()

    # Create the command
    command = (
        f'find "{args.path}" -mindepth {args.mindepth} -maxdepth {args.maxdepth} -type f '
        f'-exec stat --format=\'%Y %n\' {{}} + | sort -n | tail -n {args.count} | '
        f'while read -r time file; do echo "$(date -d @$time "+%Y-%m-%d %H:%M:%S") $file"; done'
    )

    # Print the command
    print(command)


if __name__ == "__main__":
    generate_command()
