import re
import subprocess
import argparse
from trusted_ips import trusted_ips


def ip_to_int(*, ip):
    """Convert an IP address to integer for easier comparison."""
    return int("".join([f"{int(i):08b}" for i in ip.split(".")]), 2)


def is_local_ip(*, ip, private_ip_ranges, special_ips):
    """Check if IP is in a specified range."""
    ip_int = ip_to_int(ip=ip)
    for start, end in private_ip_ranges:
        if ip_to_int(ip=start) <= ip_int <= ip_to_int(ip=end):
            return True
    return ip in special_ips


def get_ip_regex():
    return r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"


def get_ip_log():
    # Read the content of the auth.log
    with open("/var/log/auth.log", "r") as f:
        lines = f.readlines()

    # Extract IP addresses from sshd related logs
    ip_regex = get_ip_regex()
    ips = [
        re.search(ip_regex, line).group(0)
        for line in lines
        if "sshd" in line and re.search(ip_regex, line)
    ]

    # Unique IPs
    unique_ips = list(set(ips))
    return unique_ips


def get_banned_ips():
    # Get the list of banned IPs from fail2ban
    cmd = "sudo fail2ban-client status sshd | grep 'Banned IP list:'"
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    output, _ = process.communicate()
    banned_lines = output.decode().split("\n")
    banned_lines = [e for e in banned_lines if e != ""]

    banned_ips = []
    prefix = "Banned IP list:"
    for line in banned_lines:
        ip_addresses = line.split(prefix)[-1].strip().split(" ")
        ip_addresses = [ip.strip() for ip in ip_addresses if ip.strip() != ""]
        banned_ips.extend(ip_addresses)

    return banned_ips


def get_potential_local(*, ips, private_ip_ranges, special_ips):
    potential_local = [
        ip
        for ip in ips
        if is_local_ip(
            ip=ip, private_ip_ranges=private_ip_ranges, special_ips=special_ips
        )
    ]
    return potential_local


def get_jail_info(*, private_ip_ranges, special_ips):
    ips = get_ip_log()
    banned_ips = get_banned_ips()
    potential_local = get_potential_local(
        ips=ips, private_ip_ranges=private_ip_ranges, special_ips=special_ips
    )
    recently_jailed = [ip for ip in ips if ip in banned_ips]
    possible_hackers = [
        ip
        for ip in ips
        if ip not in potential_local and ip not in recently_jailed
    ]
    d = {
        "ips": ips,
        "banned_ips": banned_ips,
        "potential_local": potential_local,
        "recently_jailed": recently_jailed,
        "possible_hackers": possible_hackers,
    }
    return d


def report_jail(
    *, potential_local, banned_ips, recently_jailed, possible_hackers
):
    # Print Results
    print("*" * 80)
    print("POTENTIAL LOCAL")
    for ip in potential_local:
        print(ip)
    print("*" * 80)
    print("\n")

    print(80 * "-")
    print("FULL JAIL LIST")
    for ip in banned_ips:
        print(ip)
    print(80 * "-")
    print("\n")

    print("#" * 80)
    print("RECENTLY JAILED")
    for ip in recently_jailed:
        print(ip)
    print("#" * 80)
    print("\n")

    print("@" * 80)
    print("POTENTIAL HACKERS (CONSIDER JAILING IMMEDIATELY)")
    for ip in possible_hackers:
        print(ip)
    print("@" * 80)
    print("\n")


def dialogue_jail(*, possible_hackers, interactive=True):
    if len(possible_hackers) == 0:
        print(80 * "=")
        print("No potential hackers found.")
        print(80 * "=")
    else:
        fail2ban_response = get_input(
            "Go through fail2ban purge dialogue?", interactive=interactive
        )
        if fail2ban_response:
            fail2ban_response = get_input(
                "Are you sure? BE CAREFUL IF YOU ARE DOING THIS REMOTELY!",
                interactive=interactive,
            )
        if fail2ban_response:
            for hacker_ip in possible_hackers:
                take_action = get_input(
                    f'Ban "{hacker_ip}"?', interactive=interactive
                )
                if take_action:
                    cmd = f"sudo fail2ban-client set sshd banip {hacker_ip}"
                    process = subprocess.Popen(
                        cmd,
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                    )
                    output, error = process.communicate()
                    if process.returncode == 0:
                        print(f"    Successfully banned {hacker_ip}")
                    else:
                        print(
                            f"Error banning {hacker_ip}. Error:"
                            f" {error.decode()}"
                        )


def get_firewall_candidates(*, jail):
    cmd = "sudo ufw status numbered | grep 'SCALPEL_DENY'"
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    output, error = process.communicate()
    firewalled_lines = output.decode().split("\n")
    firewalled_lines = [e for e in firewalled_lines if e != ""]

    ip_regex = get_ip_regex()

    firewalled_ips = [
        re.search(ip_regex, line).group(0)
        for line in firewalled_lines
        if re.search(ip_regex, line)
    ]

    # Compute jailed but not firewalled IPs
    jailed_but_not_firewalled = list(set(jail) - set(firewalled_ips))
    return firewalled_ips, jailed_but_not_firewalled


def report_firewall(*, firewalled_ips, jailed_but_not_firewalled):
    print("%" * 80)
    print("CURRENTLY FIREWALLED")
    for ip in firewalled_ips:
        print(ip)
    print("%" * 80)
    print("\n")

    print("^" * 80)
    print("JAILED BUT NOT FIREWALLED")
    for ip in jailed_but_not_firewalled:
        print(ip)
    print("^" * 80)
    print("\n")


def add_to_ufw(*, ip):
    cmd = f"sudo ufw deny from {ip} comment 'SCALPEL_DENY'"
    process = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    _, error = process.communicate()
    if process.returncode == 0:
        print(f"    Successfully added {ip} to UFW firewall.")
    else:
        print(f"    Error adding {ip} to UFW firewall. Error: {error.decode()}")


def dialogue_firewall(*, jailed_but_not_firewalled, interactive=True):
    if len(jailed_but_not_firewalled) > 0:
        firewall_response = get_input(
            "Would you like to firewall the currently jailed items also?",
            interactive=interactive,
        )

        if firewall_response:
            firewall_response = get_input(
                "Are you sure? BE CAREFUL IF YOU ARE DOING THIS REMOTELY!",
                interactive=interactive,
            )
        if firewall_response:
            for jailed_ip in jailed_but_not_firewalled:
                add_to_ufw(ip=jailed_ip)
        else:
            print("Exiting without firewalling any IPs.")
    else:
        print("No IPs to firewall.")


def get_input(prompt, *, yes="y", no="n", interactive=True):
    clean_prompt = (
        prompt.strip()
        .replace("?", "")
        .replace(f"({yes}/{no})", "")
        .replace(f"(yes -> {yes}/no -> {no})", "")
        .strip()
    )
    clean_prompt = f"{clean_prompt} ({yes}/{no})? "
    if not interactive:
        print(f"{clean_prompt} {yes} (non-interactive mode)")
        return True
    if yes.lower() != yes or no.lower() != no:
        raise ValueError("yes and no must be lowercase, got {yes} and {no}")
    response = input(clean_prompt).strip().lower()
    if response == yes:
        return True
    elif response == no:
        return False
    else:
        print(f'Invalid response. Please enter "{yes}" or "{no}".')
        return get_input(prompt=prompt, yes=yes, no=no)


def main():
    parser = argparse.ArgumentParser(description="Auto jail and firewall IPs.")
    parser.add_argument(
        "--noninteractive",
        "-n",
        action="store_true",
        help="Enable interactive mode.",
    )
    args = parser.parse_args()
    args.interactive = not args.noninteractive

    # Classify IPs
    # Special IPs and Private IP ranges
    # Should be located in this .trusted_ips.py file
    special_ips, private_ip_ranges = trusted_ips()

    jail_info = get_jail_info(
        private_ip_ranges=private_ip_ranges, special_ips=special_ips
    )
    del jail_info["ips"]

    report_jail(**jail_info)

    dialogue_jail(
        possible_hackers=jail_info["possible_hackers"],
        interactive=args.interactive,
    )

    # update jail info since newly jailed IPs may have been added
    jail_info = get_jail_info(
        private_ip_ranges=private_ip_ranges, special_ips=special_ips
    )

    (
        firewalled_ips,
        recently_jailed_but_not_firewalled,
    ) = get_firewall_candidates(jail=jail_info["recently_jailed"])

    report_firewall(
        firewalled_ips=firewalled_ips,
        jailed_but_not_firewalled=recently_jailed_but_not_firewalled,
    )

    dialogue_firewall(
        jailed_but_not_firewalled=recently_jailed_but_not_firewalled,
        interactive=args.interactive,
    )


if __name__ == "__main__":
    main()
