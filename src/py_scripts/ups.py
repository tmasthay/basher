import re


def sco(s):
    return co(s, shell=True).decode('utf-8').strip()


def main():
    s = open('setup.py').read()
    m = re.search(r'version="(.+?)"', s)
    if not m:
        raise Exception('Could not find version in setup.py')
    version = m.group(1)
    new_version = int(version.split('.')[-1]) + 1
    new_version = '.'.join(version.split('.')[:-1] + [str(new_version)])
    s = s.replace(version, new_version)
    with open('setup.py', 'w') as f:
        f.write(s)


if __name__ == "__main__":
    main()
