import os
from rich.console import Console
from rich.traceback import install
import sys
from shutil import get_terminal_size as gts


cols, _ = gts(fallback=(80, 24))
if cols == 0:
    cols = os.environ.get('COLUMNS', 80)

filename = os.environ.get('RICH_LOG', '')
if filename.lower() != 'none':
    if not filename:
        file = sys.stdout
    else:
        file = open(filename, 'wt')

    console = Console(file=file, force_terminal=True)
    # install(
    #     console=console,
    #     show_locals=True,
    #     word_wrap=False,
    #     width=cols,
    #     locals_max_string=cols,
    #     locals_max_length=20,
    # )

    install(
        console=console,
        show_locals=os.environ.get('RICH_LOCALS', '').lower() == 'true',
        word_wrap=False,
        width=cols,
        locals_max_length=10,
        locals_max_string=cols,
    )
