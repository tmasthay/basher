import random
from rich.console import Console
from rich.text import Text
import sys


def colorize_yaml(lines, depth_color_map, value_color):
    colored_lines = Text()
    for line in lines:
        # Detect the indentation level
        stripped_line = line.lstrip()
        indent_level = (len(line) - len(stripped_line)) // 2

        # Determine the color based on the indentation level
        color = depth_color_map.get(indent_level, 'white')

        # Apply the color to the line without changing the indentation
        if ':' in stripped_line:  # Key-value pair
            key, value = stripped_line.split(':', 1)
            colored_lines.append(
                ' ' * (indent_level * 2)
            )  # Preserve indentation
            colored_lines.append(key + ': ', style=color)
            colored_lines.append(value.strip(), style=value_color)
        elif stripped_line.startswith('-'):  # List item
            colored_lines.append(
                ' ' * (indent_level * 2)
            )  # Preserve indentation
            colored_lines.append(stripped_line, style=value_color)
        else:  # Handle keys without a value
            colored_lines.append(
                ' ' * (indent_level * 2)
            )  # Preserve indentation
            colored_lines.append(stripped_line, style=color)
        colored_lines.append('\n')
    return colored_lines


def main():
    console = Console()
    group1 = ['cyan', 'magenta', 'blue', 'green', 'yellow']
    group2 = [
        'bright_cyan',
        'bright_magenta',
        'bright_blue',
        'bright_green',
        'bright_yellow',
    ]
    group3 = [
        'orange3',
        'dark_violet',
        'medium_purple3',
        'chartreuse',
        'deep_pink3',
    ]
    group4 = [
        'gold3',
        'dark_orange',
        'medium_turquoise',
        'dark_sea_green',
        'light_coral',
    ]
    groups = [group1, group2, group3, group4]
    if len(sys.argv) == 1:
        order = range(4)
    elif sys.argv[1] == 'rand':
        order = list(range(4))
        random.shuffle(order)
    else:
        order = [int(i) for i in sys.argv[1].split(',')]
    print(order)
    import os

    os.system('sleep 5')
    colors = []
    for i in order:
        colors.extend(groups[i])
    depth_color_map = {i: color for i, color in enumerate(colors)}
    value_color = 'red'

    # Read the input and split into lines while removing unwanted parts
    input_lines = sys.stdin.read().strip().split('\n')
    processed_lines = []
    start_processing = False
    for line in input_lines:
        if line.strip().endswith("is powered by Hydra."):
            start_processing = True
            continue
        if line.strip().startswith("Powered by Hydra"):
            break
        if start_processing:
            processed_lines.append(line)

    # Colorize the lines while preserving indentation
    colored_output = colorize_yaml(
        processed_lines, depth_color_map, value_color
    )
    console.print(colored_output)


if __name__ == "__main__":
    main()
