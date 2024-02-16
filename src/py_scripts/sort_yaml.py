import yaml
import sys

# auy.py -> "auto update yaml"


def main():
    if len(sys.argv) == 1:
        filename = 'cfg/cfg.yaml'
    else:
        filename = sys.argv[1]
    filename = filename.replace('.yaml', '') + '.yaml'
    with open(filename, "r") as f:
        data = yaml.safe_load(open(filename, "r"))
    with open(filename, "w") as f:
        yaml.dump(data, f, default_flow_style=None, sort_keys=True)
    with open(filename, "r") as f:
        print(f'YAML {filename} updated:\n{f.read()}')


if __name__ == "__main__":
    main()
