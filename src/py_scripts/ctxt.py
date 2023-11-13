# colorize_text.py
import argparse
import re
import sys
import os


def gcl(color):
    # Standard colors
    colors = {
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "reset": "\033[0m",
    }

    # RGB colors (rgbXYZ format)
    rgb_match = re.match(r'rgb([0-5])([0-5])([0-5])', color)
    if rgb_match:
        r, g, b = map(int, rgb_match.groups())
        code = 16 + (36 * r) + (6 * g) + b
        return f"\033[38;5;{code}m"

    # Grayscale colors (grayN format)
    gray_match = re.match(r'gray([0-9]+)', color)
    if gray_match:
        gray_value = int(gray_match.group(1))
        if 0 <= gray_value <= 23:
            code = 232 + gray_value
            return f"\033[38;5;{code}m"

    return colors.get(color, "\033[37m")  # Default to white if color is unknown


def ctxt(text, color):
    color_code = gcl(color)
    reset_code = gcl("reset")
    text = bytes(text, "utf-8").decode("unicode_escape")
    return f"{color_code}{text}{reset_code}"


def colorize_text(text, separator, colors):
    if separator is None:
        return ctxt(text, colors[0])
    else:
        parts = text.split(separator)
        colored_parts = [
            ctxt(part, colors[i % len(colors)]) for i, part in enumerate(parts)
        ]
        return separator.join(colored_parts)


def main():
    parser = argparse.ArgumentParser(description="Colorize text")
    parser.add_argument("text", type=str, help="Text to colorize")
    parser.add_argument(
        "-s",
        "--sep",
        type=str,
        default='\n',
        help="Separator to split text, default is None",
    )
    parser.add_argument(
        '-n', '--no-sep', action='store_true', help='Do not split text'
    )
    parser.add_argument(
        "-c",
        "--colors",
        nargs='+',
        default=["white"],
        help="List of colors, default is ['white']",
    )
    parser.add_argument(
        '-l', '--literal', action='store_true', help='Read text from file'
    )
    parser.add_argument('-t', '--theme', type=str, help='color theme from file')

    args = parser.parse_args()
    if not args.literal:
        args.text = open(args.text, 'r').read()
    if args.no_sep:
        args.sep = None
    if args.sep is not None:
        args.sep = bytes(args.sep, "utf-8").decode("unicode_escape")
    args.text = bytes(args.text, 'utf-8').decode('unicode_escape')

    # input(args)
    if args.theme is not None:
        basher = os.environ['BASHER']
        args.colors = open(f'{basher}/themes/{args.theme}.cth').read().split()
        args.colors = [e for e in args.colors if e not in ['-c', '--colors']]

    input(args)
    colored_text = colorize_text(args.text, args.sep, args.colors)
    print(colored_text)


if __name__ == "__main__":
    main()
