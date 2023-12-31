from subprocess import check_output as co
import argparse
import os
from datetime import datetime


def sco(cmd, split=False):
    res = co(cmd, shell=True).decode("utf-8").strip()
    if split:
        return res.split("\n")
    else:
        return res


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--basher', type=str, required=True)
    parser.add_argument("--interval", "-i", type=int, default=60)
    parser.add_argument("--num_intervals", "-N", type=int, default=24)
    parser.add_argument(
        "--out", "-o", type=str, default="/home/tyler/jobs/ufw_monitor"
    )

    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)

    python3 = sco('which python3')
    blist = (
        'sudo'
        f' {python3} {os.path.join(args.basher, "src/py_scripts/check_jail.py")}'
    )
    input(blist)
    for j in range(args.num_intervals):
        i = j * args.interval + 1
        at_cmd = f"at now + {i} minutes 2> /dev/null"
        timestamp = sco(f"date -d \"+{i} minutes\" +'%Y_%m_%d_%H_%M_%S'")
        stdout_file = os.path.join(args.out, f"{timestamp}.out")
        stderr_file = os.path.join(args.out, f"{timestamp}.err")
        base_cmd = f"{blist} -n > {stdout_file} 2> {stderr_file}"
        base_cmd = f"echo '{base_cmd}'"
        cmd = f"{base_cmd} | {at_cmd}"
        print(f"{cmd}")
        os.system(cmd)
    print("WARNING: at command will run in /bin/sh, not /bin/bash!")


if __name__ == "__main__":
    main()
