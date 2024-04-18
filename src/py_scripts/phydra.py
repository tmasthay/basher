import sys


def process_help_text(text):
    # This function is where you'd add your logic to colorize or process the text
    # For demonstration, it just prints the text
    print(text)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'stdin':
        # Read standard input (stdin)
        text = sys.stdin.read()
        process_help_text(text)
    else:
        print(
            "This script expects 'stdin' as the argument to read from standard input."
        )


if __name__ == "__main__":
    main()
