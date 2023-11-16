import argparse
import os
import time

def get_args():
    parser = argparse.ArgumentParser(description='Combine table outputs from multiple processes.')
    parser.add_argument('world_size', type=int, nargs='?', default=2, help='The number of files (processes) to read from. Defaults to 2.')
    parser.add_argument('--sep', default='     ', help='Separator string. Default is five spaces.')
    parser.add_argument('--base', default='/tmp/tmp', help='Base file path. Default is /tmp/tmp.')
    parser.add_argument('--ext', default='txt', help='File extension. Default is txt.')
    parser.add_argument('-r', '--refresh-rate', type=int, default=2, help='Refresh rate in seconds. Defaults to 3.')
    parser.add_argument('-N', '--num-views', type=int, default=10000, help='Number of refreshes to run. Defaults to 100.')
    return parser.parse_args()

def read_and_combine_tables(base, world_size, ext, sep):
    rank_strings = []
    for rank in range(world_size):
        try:
            with open(f'{base}{rank}.{ext}', 'r') as file:
                rank_strings.append(file.read().strip().split('\n'))
        except FileNotFoundError:
            rank_strings.append([""])
    
    # Pad the lists of lines so they all have the same length
    max_lines = max(len(lines) for lines in rank_strings)
    for lines in rank_strings:
        lines.extend([''] * (max_lines - len(lines)))
    
    # Join corresponding lines from each file with the separator
    combined_lines = [sep.join(rank_lines[i] for rank_lines in rank_strings) for i in range(max_lines)]
    
    return '\n'.join(combined_lines)

def clear_screen():
    print('\033[H\033[J', end='')

if __name__ == "__main__":
    args = get_args()
    for _ in range(args.num_views):
        combined_string = read_and_combine_tables(args.base, args.world_size, args.ext, args.sep)
        clear_screen()
        print(combined_string)
        time.sleep(args.refresh_rate)

