import pandas as pd
import sys
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+', type=str)
    parser.add_argument('-o', '--out', type=str, default='out.csv')
    parser.add_argument(
        '-t',
        '--transpose',
        action='store_true',
        help='Transpose the file',
    )
    parser.add_argument('-n', '--no-save', action='store_true')
    parser.add_argument('-w', '--width', default=20, type=int)
    parser.add_argument('-s', '--sep', default=',', type=str)
    parser.add_argument('-q', '--quiet', action='store_true')
    args = parser.parse_args()
    for i, file in enumerate(args.files):
        if not file.endswith('.csv'):
            if '.' in file:
                raise ValueError(f"File must end with '.csv'")
            else:
                args.files[i] += '.csv'
    return args


def main():
    args = get_args()

    # Initialize an empty DataFrame
    combined_df = None

    for file in args.files:
        # Read each file
        df = pd.read_csv(file, sep=args.sep)
        if args.transpose:
            df = df.T

        # Check if combined_df is not None, then concatenate, else assign df to combined_df
        if combined_df is not None:
            # Ensuring the first column matches between the two DataFrames
            assert (combined_df.iloc[:, 0] == df.iloc[:, 0]).all()
            # Concatenate all columns except the first one
            combined_df = pd.concat([combined_df, df.iloc[:, 1:]], axis=1)
        else:
            combined_df = df

    # Saving and/or printing
    if not args.no_save:
        combined_df.to_csv(args.out, index=False)
        with open(args.out.replace('.csv', '.txt'), 'w') as f:
            f.write(combined_df.to_string(col_space=args.width, index=False))

    if not args.quiet:
        print(combined_df.to_string(col_space=args.width, index=False) + '\n')


if __name__ == '__main__':
    main()
