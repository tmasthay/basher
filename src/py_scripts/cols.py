from tabulate import tabulate as tab
import sys
import argparse
import numpy as np


def main():
    parser = argparse.ArgumentParser(description='Columnizes a list of words')
    parser.add_argument('--cols', '-c', type=int, default=10, help='Columns')
    parser.add_argument('list', nargs='*', help='List of words')
    args = parser.parse_args()

    full_list = []
    for e in args.list:
        if e != '':
            full_list.extend(e.split())

    final = np.array_split(full_list, int(np.ceil(len(full_list) // args.cols)))
    final = [list(e) for e in final]

    print(tab(final, tablefmt='plain'))


if __name__ == '__main__':
    main()
