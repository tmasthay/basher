from subprocess import check_output as co
import os
import argparse
from masthay_helpers.global_helpers import ctab


def sco(cmd):
    return co(cmd, shell=True).decode('utf-8').strip()


def main():
    repo_root = sco("git rev-parse --show-toplevel")
    new_path = os.path.join(repo_root, 'worktrees')
    os.chdir(new_path)

    base_find = 'find . -type f'
    base_grep = 'grep -Hno --color=always'

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--find_args', type=str, default='')
    parser.add_argument('-g', '--grep_args', type=str, default='')
    parser.add_argument('--clean', action='store_true')
    parser.add_argument('--colors', type=str, default=None)
    args = parser.parse_args()

    if args.colors:
        args.colors = args.colors.split(',')

    if not args.clean:
        args.find_args = f'{base_find} {args.find_args.strip()}'
        args.grep_args = f'{base_grep} {args.grep_args.strip()}'

    cmd = f'{args.find_args} -exec {args.grep_args} ' + '{} \;'
    cmd += " | sed 's/[.]\///'"
    res = sco(cmd)

    if args.clean:
        print(res)
        return

    data = []
    for e in res.split('\n'):
        tokens = e.split(':')
        if len(tokens) < 3:
            print(
                f'SOMETHING WENT WRONG ONLY SAW {len(tokens)} tokens...here is'
                ' raw output\n'
            )
            print(res)
            return
        tokens = [tokens[0], tokens[1], ':'.join(tokens[2:])]

        path, line, text = tokens
        split_path = path.split('/')
        branch = split_path[0]
        true_path = '/'.join(split_path[1:])
        data.append([branch, true_path, line, text])

    s = ctab(
        data, headers=['BRANCH', 'PATH', 'LINE', 'TEXT'], colors=args.colors
    )
    print(s)


if __name__ == "__main__":
    main()
