import pydoc
import sys
import importlib
from subprocess import check_output as co
import os


# # Function to add ANSI color codes to text
# def colorize_text(text):
#     # Replace standard doc headers with colorized versions
#     headers = [
#         'NAME',
#         'FILE',
#         'MODULE DOCS',
#         'DESCRIPTION',
#         'CLASSES',
#         'FUNCTIONS',
#         'DATA',
#     ]
#     for header in headers:
#         text = text.replace(header, f'\x1b[1m\x1b[4m{header}\x1b[0m')
#     return text


# # Function to print the colorized documentation for a module
# def colorize_docstring(module):
#     docstring = pydoc.plain(pydoc.render_doc(module))
#     return colorize_text(docstring)


# if __name__ == '__main__':
#     if len(sys.argv) < 2:
#         print("Usage: phelp.py <module_name>")
#         sys.exit(1)

#     module_name = sys.argv[1]

#     try:
#         # Import the module with full dotted path
#         if '.' in module_name:
#             module = importlib.import_module(module_name)
#         else:
#             module = __import__(module_name)

#         # Print the colorized help text
#         print(colorize_docstring(module))
#     except ModuleNotFoundError:
#         print(f"Module '{module_name}' not found.")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# arg = sys.argv[1]
# pkg = arg.split(".")[0]
# mod = arg.split(".")[1]
# u = f"python -c 'from {pkg} import {mod}; print({mod}.__doc__)'"
# os.system(u)
import sys
import importlib


def get_help_as_string(obj):
    """
    Get the help information for an object as a string.
    """
    import io
    from contextlib import redirect_stdout

    help_io = io.StringIO()
    with redirect_stdout(help_io):
        help(obj)
    return help_io.getvalue()


if __name__ == "__main__":
    module_name = sys.argv[1]

    # Split the module name by dots
    parts = module_name.split('.')

    # Try to import the module or object dynamically
    try:
        if len(parts) == 1:
            # If there is no dot, import the module directly
            module = importlib.import_module(module_name)
            help_text = get_help_as_string(module)
        else:
            # If there is a dot, import the parent module
            # and then get the attribute (the last part)
            module = importlib.import_module('.'.join(parts[:-1]))
            obj = getattr(module, parts[-1])
            help_text = get_help_as_string(obj)

        print(help_text)
    except (ModuleNotFoundError, AttributeError) as e:
        print(f"Error: {e}")
