import os
from os.path import join as pj


commands = {
    'cdi': 'ISL',
    'cdb': 'BASHER',
    'cdmh': pj('REPO', 'masthay_helpers'),
    'cdh': 'HOME',
    'cdj': 'JOBS',
    'cdr': 'REPO',
    'cda': pj('ISL', 'misfit_toys', 'ref_hydra')
}


def generate_script(*, template_path, output_path):
    with open(template_path, 'r') as file:
        template_content = file.read()

    output_content = "#!/bin/bash\n\n"

    funcs = []
    completions = []
    for func_name, env_var in commands.items():
        func_content = template_content.replace('@@@FUNC_NAME@@@', func_name)
        if env_var.startswith('/'):
            func_content = func_content.replace('$@@@PATH_CONTEXT@@@', env_var)
        else:
            func_content = func_content.replace('@@@PATH_CONTEXT@@@', env_var)
        funcs.append(func_content)
        completions.append(f"complete -F _{func_name} {func_name}")

    with open(output_path, 'w') as file:
        final_content = (
            output_content
            + "\n\n".join(funcs)
            + '\n\n'
            + '\n'.join(completions)
        )
        file.write(final_content)

    print(f"Script generated at {os.path.abspath(output_path)}")


if __name__ == "__main__":
    generate_script(
        template_path='path_template.sh', output_path='path_complete.sh'
    )
