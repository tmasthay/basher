from subprocess import check_output as co
import sys
import argparse
import os
from rich.table import Table
from rich.console import Console

def sco(cmd, *, verbose=False):
    if verbose:
        print(f"Running command: {cmd}", file=sys.stderr)
    return co(cmd, shell=True).decode('utf-8').strip()

def str_to_emoji(s, d):
    return d.get(s, d['default'])

def out_to_emoji(complete, status):
    d_complete = {
        'in_progress': '🔄',
        'completed': None,
        'default': '❓',
    }
    d_status = {
        'success': '✅',
        'failure': '❌',
        'cancelled': '🚫',
        'default': '❓',
    }
    s1 = str_to_emoji(complete, d_complete)
    return str_to_emoji(status, d_status) if s1 is None else s1

def get_branch_output(branch, *, workflow=None, limit=5):
    workflow_cmd = '' if workflow is None else f"--workflow '{workflow}'"
    limit_cmd = '' if limit is None else f"--limit {limit}"
    cmd = f"gh run list --branch {branch} {workflow_cmd} {limit_cmd} | awk '{{print $1, $2}}'"
    out = [e.split() for e in sco(cmd).split('\n')]
    out = [out_to_emoji(*e) for e in out]
    return out

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--branches', nargs='+', help='Branches to check', default=None)
    parser.add_argument('-w', '--workflow', help='Workflow to check', default="GPU Validation and Docs Deployment Workflow")
    parser.add_argument('-l', '--limit', type=int, help='Limit the number of branches to check', default=None)
    args = parser.parse_args()
    
    if args.workflow is None or args.workflow == 'null':
        args.workflow = os.environ.get('ISL_CI_RUN_WORKFLOW', None)
    if args.branches is None:
        args.branches = os.environ.get('ISL_CI_RUN_BRANCHES', 'main,devel')
    elif args.branches.lower() == 'all':
        args.branches = sco("git ls-remote --heads $(git config --get remote.origin.url) | awk '{print $2}' | sed 's|refs/heads/||g'")
        args.branches = ','.join(e for e in args.branches.split('\n') if e)
    if args.limit is None:
        args.limit = int(os.environ.get('ISL_CI_RUN_LIMIT', 5))
    args.branches = args.branches.split(',')
    return args

def main(args):
    d = {}
    for branch in args.branches:
        d[branch] = get_branch_output(branch, workflow=args.workflow, limit=args.limit)
        
        # extend them to length args.limit with empty strings if necessary
        d[branch] += [''] * (args.limit - len(d[branch]))

    console = Console()
    header_color = "bold magenta"
    row_kw = {'style': 'cyan', 'justify': 'right', 'no_wrap': True}
    table = Table(show_header=True, header_style=header_color)
    table.add_column("Run", **row_kw)
    for branch in d.keys():
        table.add_column(branch, style="magenta")
    for i in range(args.limit):
        row = [f"Run {i+1}"]
        for branch, runs in d.items():
            row.append(runs[i])
        table.add_row(*row)

    console.print(table)

if __name__ == "__main__":
    main(get_args())
    


