import argparse
import pandas as pd


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
    parser.add_argument('-n', '--no-save', action='store_true')

    args = parser.parse_args()
    if args.dest is None:
        args.dest = args.file.replace('.csv', '_stats.csv')
    if not args.dest.endswith('.csv'):
        raise ValueError(f"Destination file must end with '.csv'")
    return args


def main():
    args = get_args()

    # Read the CSV file using pandas
    df = pd.read_csv(args.file, index_col=False)

    # Compute the requested statistics
    stats_df = compute_stats(df, args.stats)

    # Save the statistics DataFrame to a CSV file
    if not args.no_save:
        stats_df.to_csv(args.dest, index_label='STAT')
        with open(args.dest.replace('.csv', '.txt'), 'w') as f:
            f.write(stats_df.to_string())
        print('Data saved in ' + args.dest)

    print(stats_df.to_string() + '\n')


if __name__ == '__main__':
    main()
