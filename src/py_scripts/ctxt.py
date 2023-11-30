# colorize_text.py
import argparse
import re

# import sys
import os
from random import randint as rand


def colormap_closure():
    ansi_map = {
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
    base_map = {
        'orange': 'rgb530',
        'maroon': 'rgb513',
        'olive': 'rgb330',
        'navy': 'rgb003',
        'teal': 'rgb033',
        'lime': 'rgb250',
        'coral': 'rgb522',
        'salmon': 'rgb520',
        'beige': 'rgb542',
        'mint': 'rgb253',
        'lavender': 'rgb432',
        'plum': 'rgb302',
        'indigo': 'rgb214',
        'gold': 'rgb530',
        'pink': 'rgb532',
        'tan': 'rgb531',
        'coffee': 'rgb321',
        'chocolate': 'rgb320',
        'azure': 'rgb006',
        'silver': 'rgb555',
    }

    def helper():
        x, y, z = rand(0, 5), rand(0, 5), rand(0, 5)
        return ansi_map, {**base_map, 'rand': f'rgb{x}{y}{z}'}

    return helper


colormap = colormap_closure()


def gcl(color):
    ansi_map, human_map = colormap()

    if color in ansi_map.keys():
        return ansi_map[color]

    if color in human_map.keys():
        color = human_map[color]
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

    return "\033[37m"


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
        '-e', '--empty', action='store_true', help='Do not end with newline'
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

    colored_text = colorize_text(args.text.strip(), args.sep, args.colors)
    end = '\n'
    if args.empty:
        end = ''
    print(colored_text, end=end)


if __name__ == "__main__":
    main()
