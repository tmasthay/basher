import subprocess as subp
import sys
from datetime import datetime


def run_command(command, message):
    if type(command) == str:
        command = command.split()
    print(f"{message}\nCommand to run: {' '.join(command)}")
    confirmation = input("Proceed? (y/n): ")
    if confirmation.lower() == 'y':
        result = subp.run(
            command, stdout=subp.PIPE, stderr=subp.PIPE, text=True
        )
        if result.returncode == 0:
            print(result.stdout)
        else:
            print("Error:", result.stderr)
            sys.exit(-1)
    else:
        print("Operation cancelled.")
        sys.exit(-1)


def main():
    protected_branches = ["main", "master", "devel", "experimental"]
    if len(sys.argv) < 2:
        print("Usage: python script.py <branch-name>")
        sys.exit(-1)

    branch = sys.argv[1]
    if branch in protected_branches:
        print(f"Branch {branch} is protected...exiting")
        sys.exit(-1)

    # Ensure the current branch is 'main'
    current_branch = (
        subp.check_output(['git', 'branch', '--show-current'])
        .strip()
        .decode('utf-8')
    )
    if current_branch != "main":
        print(
            "Current branch is not 'main'. Please switch to 'main' before running this script."
        )
        sys.exit(-1)

    branch_under = branch.replace('/', '_')
    date_str = datetime.now().strftime("%Y_%m_%d")
    tag_name = f"archive-{branch_under}-{date_str}"

    # Steps for archival workflow with user confirmation
    run_command(['git', 'checkout', branch], f"Checking out branch {branch}.")
    run_command(
        ['git', 'tag', '-a', tag_name, '-m', f'"Archiving {branch_under}"'],
        f"Tagging the branch as {tag_name}.",
    )
    run_command(
        ['git', 'push', 'origin', tag_name],
        f"Pushing tag {tag_name} to remote.",
    )
    run_command(['git', 'checkout', 'main'], "Switching back to main.")
    run_command(
        ['git', 'branch', '-D', branch], f"Deleting local branch {branch}."
    )
    run_command(
        ['git', 'push', 'origin', '--delete', branch],
        f"Deleting remote branch {branch}.",
    )


if __name__ == "__main__":
    main()
