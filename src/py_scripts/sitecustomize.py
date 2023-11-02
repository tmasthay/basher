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

repo_path = os.environ['REPO']
nondefault = ['GitHookEm', 'Experiments']
repos = [os.path.join(repo_path, e) for e in os.listdir(repo_path) if not e.startswith('.') and not e in nondefault and os.path.isdir(os.path.join(repo_path, e))]

for repo in repos:
    sys.path.append(repo)