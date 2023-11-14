import argparse
import pandas as pd
import re


def compute_stats(df, stats):
    # Calculate statistics and return as a new DataFrame
    result_df = pd.DataFrame()
    for stat in stats:
        if stat == 'mean':
            result_df['mean'] = df.mean()
        elif stat == 'stddev':
            result_df['stddev'] = df.std()
        elif stat == 'min':
            result_df['min'] = df.min()
        elif stat == 'max':
            result_df['max'] = df.max()
        elif stat == 'median':
            result_df['median'] = df.median()
    return result_df


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'file', type=str, help='File to load and compute stats for'
    )
    parser.add_argument(
        '-d', '--dest', type=str, default=None, help='Destination file'
    )
    parser.add_argument(
        '-s',
        '--stats',
        type=str,
        nargs='+',
        default=['mean', 'stddev', 'min', 'max', 'median'],
        help='List of stats to include',
    )
    parser.add_argument(
        '-t',
        '--transpose',
        action='store_true',
        help='Transpose the statistics DataFrame',
    )
    parser.add_argument('-n', '--no-save', action='store_true')
    parser.add_argument('-w', '--width', default=20, type=int)

    args = parser.parse_args()
    if not args.file.endswith('.csv'):
        if '.' in args.file:
            raise ValueError(f"File must end with '.csv'")
        else:
            args.file += '.csv'
    if args.dest is None:
        args.dest = args.file.replace('.csv', '_stats.csv')
    return args


def main():
    args = get_args()

    # Read the CSV file using pandas
    df = pd.read_csv(args.file, index_col=0)

    if args.transpose:
        df = df.T

    # Compute the requested statistics
    stats_df = compute_stats(df, args.stats)

    # Save the statistics DataFrame to a CSV file
    if not args.no_save:
        stats_df.to_csv(args.dest, index_label='STAT')
        with open(args.dest.replace('.csv', '.txt'), 'w') as f:
            f.write(stats_df.to_string(col_space=args.width))
        print('Data saved in ' + args.dest)

    print(stats_df.to_string(col_space=args.width) + '\n')


if __name__ == '__main__':
    main()
