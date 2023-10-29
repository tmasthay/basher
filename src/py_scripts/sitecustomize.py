from rich.console import Console
from rich.traceback import install
import os
import sys

filename = os.environ.get('RICH_LOG', '')
if filename.lower() != 'none':
    if not filename:
        file = sys.stdout
    else:
        file = open(filename, 'wt')

    dummy_width = 320
    console = Console(file=file, force_terminal=True, width=dummy_width)
    install(
        console=console,
        show_locals=True,
        word_wrap=True,
        locals_max_string=dummy_width,
        locals_max_length=dummy_width,
        width=dummy_width,
    )
