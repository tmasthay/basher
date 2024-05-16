import random
from rich.console import Console
from rich.text import Text
import sys

def create_indentation(indent_level, depth_color_map, bars=False):
    """Create indentation string, optionally with vertical bars for structure, each bar colored by depth."""
    indentation = Text()
    if bars:
        # Create a string with colored bars for each indentation level
        for i in range(indent_level):
            bar_color = depth_color_map.get(i, 'white')  # Fetch the color for the current depth
            indentation.append('| ', style=bar_color)  # Append the bar with the corresponding color
    else:
        # Standard indentation with spaces
        indentation.append(' ' * (indent_level * 2))  # Simply append spaces
    return indentation

def colorize_yaml(lines, depth_color_map, value_color, bars=True):
    colored_lines = Text()
    for line in lines:
        # Detect the indentation level
        stripped_line = line.lstrip()
        indent_level = (len(line) - len(stripped_line)) // 2

        # Generate the appropriate indentation
        indentation = create_indentation(indent_level, depth_color_map, bars)

        # Apply the color to the line without changing the indentation
        if ':' in stripped_line:  # Key-value pair
            key, value = stripped_line.split(':', 1)
            colored_lines.append(indentation)
            colored_lines.append(key + ': ', style=depth_color_map.get(indent_level, 'white'))
            colored_lines.append(value.strip(), style=value_color)
        elif stripped_line.startswith('-'):  # List item
            colored_lines.append(indentation)
            colored_lines.append(stripped_line, style=value_color)
        else:  # Handle keys without a value
            colored_lines.append(indentation)
            colored_lines.append(stripped_line, style=depth_color_map.get(indent_level, 'white'))
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
