from subprocess import check_output as co
import argparse
import os
from datetime import datetime

import sys
sys.path.append(__file__.replace("ufw_monitor.py", ""))
from trusted_ips import blist_alias


def sco(cmd, split=False):
    res = co(cmd, shell=True).decode("utf-8").strip()
    if split:
        return res.split("\n")
    else:
        return res


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval", "-i", type=int, default=60)
    parser.add_argument("--num_intervals", "-N", type=int, default=24)
    parser.add_argument(
        "--out", "-o", type=str, default="/home/tyler/jobs/ufw_monitor"
    )

    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)

    blist = blist_alias()
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
