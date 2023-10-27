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

    console = Console(file=file, force_terminal=True)
    install(
        console=console,
        show_locals=True,
        word_wrap=True,
        width=1000,
        locals_max_string=1000,
        locals_max_length=1000,
    )
