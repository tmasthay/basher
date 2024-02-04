import subprocess
import yaml
from collections.abc import MutableMapping
import hydra
from omegaconf import DictConfig
import os

# auy.py -> "auto update yaml"


def run_grep_command(name="main"):
    command = rf"grep -o 'c\.[a-zA-Z_]\+\(\.[a-zA-Z_]\+\)*' {name}.py | sed 's/c\.//g' | sort | uniq"
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    if stderr:
        print("An error occurred:", stderr.decode())
        return []

    return stdout.decode().splitlines()


def sort_keys(keys):
    # Sort based on the number of dots and then alphabetically
    return sorted(keys, key=lambda x: (x.count('.'), x))


def deep_update(source, overrides):
    """Update a nested dictionary or similar mapping.
    Modify `source` in place.
    """
    input(overrides)
    for key, value in overrides.items():
        if isinstance(value, MutableMapping) and value:
            returned = deep_update(source.get(key, {}), value)
            source[key] = returned
        else:
            source[key] = overrides[key]
    return source


def generate_yaml(
    sorted_keys,
    pre_existing_yaml="pre_existing.yaml",
    output_yaml="experiment.yaml",
):
    pre_existing_yaml = pre_existing_yaml.replace('.yaml', '') + '.yaml'
    output_yaml = output_yaml.replace('.yaml', '') + '.yaml'
    # Generate the new YAML structure
    new_config_dict = {}
    for key in sorted_keys:
        sub_keys = key.split('.')
        d = new_config_dict
        for sub_key in sub_keys[:-1]:
            if sub_key not in d:
                d[sub_key] = {}
            d = d[sub_key]
        d[sub_keys[-1]] = None  # Placeholder for actual values

    # Read the pre-existing YAML file
    try:
        input(pre_existing_yaml)
        with open(pre_existing_yaml, 'r') as f:
            pre_existing_config = yaml.safe_load(f) or {}
    except FileNotFoundError:
        pre_existing_config = {}

    # Merge the dictionaries
    merged_config = deep_update(new_config_dict, pre_existing_config)

    # Write the merged dictionary to the output YAML file
    with open(output_yaml, 'w') as f:
        yaml.dump(merged_config, f, default_flow_style=False)

    print(f"YAML file generated: {output_yaml}")


config_path = os.path.relpath(
    os.path.join(os.getcwd(), 'cfg'), start=os.path.dirname(__file__)
)
config_name = "auto_update.yaml"


@hydra.main(config_path=config_path, config_name=config_name, version_base=None)
def main(c: DictConfig):
    keys = run_grep_command(c.program)
    sorted_keys = sort_keys(keys)
    generate_yaml(sorted_keys, c.yaml, c.get("output_yaml", c.yaml))


if __name__ == "__main__":
    main()
