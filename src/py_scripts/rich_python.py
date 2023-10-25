from rich.traceback import install
import sys
import importlib
import os

# Default rich keyword arguments
rich_kwargs = {
    'theme': None,
    'width': 160,
    'extra_lines': 2,
    'word_wrap': True,
    'show_locals': True,
    'locals_max_length': 160,
    'locals_max_string': 160,
    'suppress': [],
}


# Check for the presence of the RICH_END marker
if 'RICH_END' in sys.argv:
    idx_rich_end = sys.argv.index('RICH_END')
    rich_kwargs = sys.argv[1:idx_rich_end]

    # Create the dictionary for keyword arguments from command line
    tmp = [e.split('=') for e in rich_kwargs]
    cmd_rich_dict = {e[0]: e[1] for e in tmp}

    # Update the defaults with the command-line arguments
    rich_kwargs.update(cmd_rich_dict)

    # Update sys.argv to exclude the rich_kwargs and the RICH_END marker
    sys.argv = [sys.argv[1]] + sys.argv[idx_rich_end + 1 :]
else:
    sys.argv = sys.argv[1:]

# Call install with the final set of keyword arguments
install(**rich_kwargs)

# Remove '.py' extension if present
sys.argv[0] = sys.argv[0].replace('.py', '')


sys.path.append(os.path.join(os.getcwd()))

# Determine the module and function to import
if '.' in sys.argv[0]:
    module_name, function_name = sys.argv[0].split('.', 1)
else:
    module_name = sys.argv[0]
    function_name = 'main'

# Dynamically import the module and function
module = importlib.import_module(module_name)
main_function = getattr(module, function_name)

# Execute the 'main' function
main_function()
