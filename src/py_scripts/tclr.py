import sys
from colorama import Fore, Style, init
import re

# Initialize Colorama
init(autoreset=True)

# Define colors for different depths
colors = [
    Fore.RED,
    Fore.GREEN,
    Fore.YELLOW,
    Fore.MAGENTA,
    Fore.CYAN,
    Fore.WHITE,
]


def strip_ansi(text):
    ansi_escape = re.compile(r'(?:\x1b\[|\x9b)[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)


def colorize_line(line):
    colored_line = ''
    depth = 0
    for char in line:
        colored_line += colors[depth % len(colors)] + char
        if char == '│' or char == '├' or char == '└':
            depth += 1
    return colored_line


def main():
    try:
        for line in sys.stdin:
            print(colorize_line(strip_ansi(line.rstrip())))
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()