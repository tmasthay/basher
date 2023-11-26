from rich.console import Console
from rich.traceback import install
import os
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
    install(
        console=console,
        show_locals=True,
        word_wrap=False,
        width=cols,
        locals_max_string=cols,
        locals_max_length=20,
    )

# repo_path = os.environ['REPO']
# nondefault = ['GitHookEm', 'Experiments']
# repos = [os.path.join(repo_path, e) for e in os.listdir(repo_path) if not e.startswith('.') and not e in nondefault and os.path.isdir(os.path.join(repo_path, e))]

# for repo in repos:
#     sys.path.append(repo)

# The above can simply be done by using "pip install -e ." instead
