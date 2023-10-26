from subprocess import check_output as co
import os
import argparse
from masthay_helpers.global_helpers import ctab


def sco(cmd):
    return co(cmd, shell=True).decode('utf-8').strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--find_args', type=str, default='')
    parser.add_argument('-g', '--grep_args', type=str, default='')
    parser.add_argument('-c', '--clean', action='store_true')
    args = parser.parse_args()

    base_find = 'find . -type f'
    base_grep = 'grep -Hno --color=always'

    if not args.clean:
        args.find_args = f'{base_find} {args.find_args.strip()}'
        args.grep_args = f'{base_grep} {args.grep_args.strip()}'

    input(args)

    repo_root = sco("git rev-parse --show-toplevel")
    os.chdir(repo_root)

    cmd = f'{args.find_args} -exec {args.grep_args} ' + '{} \;'
    cmd += " | sed 's/worktrees\///'"
    input(cmd)
    res = sco(cmd)
    print(res)


if __name__ == "__main__":
    main()
