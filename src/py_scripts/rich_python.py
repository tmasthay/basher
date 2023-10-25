from rich.traceback import install
import sys
import importlib
import os
import inspect
import re
from tabulate import tabulate as tab
from masthay_helpers.global_helpers import ctab, cprint, cstr, bstr


def main():
    dmr = '--'

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

    if sys.argv[1].replace('-', '').lower() in ['h', 'help']:
        help_clr = 'green'
        col_colors = ['red', 'magenta', 'yellow']
        headers = ['Argument', 'Type', 'rpython Default']
        example_clr = 'cyan'

        sig = inspect.signature(install)

        table_data = []
        # Iterate through the parameters in the signature
        for name, param in sig.parameters.items():
            arg_name = name
            type_hint = (
                str(param.annotation)
                .replace('<class ', '')
                .replace('>', '')
                .replace("'", "")
            )
            if arg_name in rich_kwargs.keys():
                default_value = rich_kwargs[arg_name]
            else:
                default_value = (
                    param.default if param.default is not param.empty else None
                )
            table_data.append([arg_name, type_hint, default_value])

        table = ctab(table_data, colors=col_colors, headers=headers)
        table = '\n'.join([8 * ' ' + e for e in table.split('\n')])
        table = bstr(
            cstr(f'USAGE: rpython [rich_kwargs] [{dmr}] ', help_clr),
            cstr('module[.main_function="main"] [cmd_line_args]\n\n', help_clr),
            cstr(
                (
                    f'    If rich_kwargs is empty, the "{dmr}" separator can be'
                    ' omitted.\n\n'
                ),
                help_clr,
            ),
            cstr('    Options for rich_kwargs:\n\n', help_clr),
            table,
            cstr('\n\n    Examples:\n', help_clr),
            cstr(
                '        rpython width=80 -- my_module.main_dummy arg1 arg2\n',
                example_clr,
            ),
        )
        print(table)

        return

    # Check for the presence of the RICH_END marker
    if dmr in sys.argv:
        idx_rich_end = sys.argv.index(dmr)
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


if __name__ == '__main__':
    main()
