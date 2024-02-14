import yaml
from collections.abc import MutableMapping
import hydra
from omegaconf import DictConfig
import os
import ast
import inspect
import re

# auy.py -> "auto update yaml"


def cfg_refs(s, equality=False):
    regex = r'c[f]*[g]*\.([a-zA-Z_]+(\.[a-zA-Z_]+)*)'
    if equality:
        regex += r'[ ]*=[ ]*'
    return set([e[0] for e in re.findall(regex, s)])


def src_code(s, function_name):
    parsed_ast = ast.parse(s)

    class FunctionVisitor(ast.NodeVisitor):
        def __init__(self):
            self.source_code = None

        def visit_FunctionDef(self, node):
            if node.name == function_name:
                # Extract line numbers
                start_line = node.lineno - 1
                end_line = (
                    node.end_lineno if hasattr(node, 'end_lineno') else None
                )

                # Extract the source code lines
                if end_line:
                    self.source_code = '\n'.join(
                        s.splitlines()[start_line:end_line]
                    )
                else:
                    # If end_lineno is not available, this method is less reliable
                    self.source_code = '\n'.join(s.splitlines()[start_line:])

    visitor = FunctionVisitor()
    visitor.visit(parsed_ast)

    return visitor.source_code


def get_valid_keys(full_src: str, function_name: str):
    all_refs = cfg_refs(full_src)
    invalid_refs = cfg_refs(src_code(full_src, function_name), equality=True)
    valid_refs = all_refs - invalid_refs
    return valid_refs


def sort_keys(keys):
    # Sort based on the number of dots and then alphabetically
    return sorted(keys, key=lambda x: (x.count('.'), x))


def deep_update(source, overrides):
    """Update a nested dictionary or similar mapping.
    Modify `source` in place.
    """
    for key, value in overrides.items():
        if isinstance(value, MutableMapping) and value:
            returned = deep_update(source.get(key, {}), value)
            source[key] = returned
        else:
            # input(f"key: {key}, value: {value}, source: {source[key]}")
            try:
                source[key] = overrides[key]
            except:
                source = {key: overrides[key]}
    return source


def generate_yaml(
    sorted_keys,
    pre_existing_yaml="pre_existing.yaml",
    output_yaml="output.yaml",
):
    pre_existing_yaml = pre_existing_yaml.replace('.yaml', '') + '.yaml'
    output_yaml = output_yaml.replace('.yaml', '') + '.yaml'
    d = yaml.safe_load(open(pre_existing_yaml, "r")) or {}
    for key in sorted_keys[::-1]:
        sub_keys = key.split('.')
        ref_d = d
        for sub_key in sub_keys[:-1]:
            if sub_key not in ref_d:
                ref_d[sub_key] = {}
            ref_d = ref_d[sub_key]
        if sub_keys[-1] not in ref_d:
            ref_d[sub_keys[-1]] = None
    with open(output_yaml, "w") as f:
        yaml.dump(d, f, default_flow_style=False, sort_keys=True)


# def generate_yaml(
#     sorted_keys,
#     pre_existing_yaml="pre_existing.yaml",
#     output_yaml="experiment.yaml",
# ):
#     pre_existing_yaml = pre_existing_yaml.replace('.yaml', '') + '.yaml'
#     output_yaml = output_yaml.replace('.yaml', '') + '.yaml'
#     # Generate the new YAML structure
#     new_config_dict = {}
#     for key in sorted_keys:
#         sub_keys = key.split('.')
#         d = new_config_dict
#         for sub_key in sub_keys[:-1]:
#             if sub_key not in d and sub_key in sorted_keys:
#                 d[sub_key] = {}
#             d = {} if d[sub_key] is None else d[sub_key]
#         d[sub_keys[-1]] = None  # Placeholder for actual values

#     # Read the pre-existing YAML file
#     try:
#         with open(pre_existing_yaml, 'r') as f:
#             pre_existing_config = yaml.safe_load(f) or {}
#     except FileNotFoundError:
#         pre_existing_config = {}

#     # Merge the dictionaries
#     merged_config = deep_update(new_config_dict, pre_existing_config)

#     # Write the merged dictionary to the output YAML file
#     with open(output_yaml, 'w') as f:
#         yaml.dump(merged_config, f, default_flow_style=None, sort_keys=True)

#     print(f"YAML file generated: {output_yaml}")


config_path = os.path.relpath(
    os.path.join(os.getcwd(), 'cfg'), start=os.path.dirname(__file__)
)
config_name = "auto_update.yaml"


@hydra.main(config_path=config_path, config_name=config_name, version_base=None)
def main(c: DictConfig):
    program = c.program.replace('.py', '') + '.py'
    src = open(program, 'r').read()
    keys = get_valid_keys(src, c.get("function_name", "derive_cfg"))
    sorted_keys = sort_keys(keys)
    generate_yaml(sorted_keys, c.yaml, c.get("output_yaml", c.yaml))


if __name__ == "__main__":
    main()
