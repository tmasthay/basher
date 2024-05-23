import os
import subprocess
import sys

def gcp(extra_excludes=[]):
    # Determine the root of the repository
    try:
        repo_root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).strip().decode('utf-8')
    except subprocess.CalledProcessError:
        print("Error: This directory is not part of a Git repository.")
        return
    
    # Path to the .gitgunk file
    gunk_file = os.path.join(repo_root, '.gitgunk')
    
    # Read the exclusions from the .gitgunk file if it exists
    excludes = []
    if os.path.isfile(gunk_file):
        with open(gunk_file, 'r') as file:
            excludes = [e.strip() for e in file.read().split('\n') if len(e.strip()) > 0]
    excludes.extend(extra_excludes)
    
    exclude_args = []
    for exclude in excludes:
        exclude_args.extend(['--exclude', exclude])

    clean_cmd = ['git', 'clean', '-idx'] + exclude_args
    print(' '.join(clean_cmd))
    subprocess.run(clean_cmd)

if __name__ == "__main__":
    gcp(sys.argv[1:])
