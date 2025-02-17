# @VS@ pc cho

import os
import subprocess
import hydra
from dotmap import DotMap
from omegaconf import OmegaConf, DictConfig
import sys
import re

def strip_ansi_codes(text):
    ansi_escape_pattern = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape_pattern.sub('', text)

def preprocess_cfg(cfg: DictConfig) -> DotMap:
    c = DotMap(OmegaConf.to_container(cfg, resolve=True))
    lt = line_transform(c.transform.line)
    ct = command_transform(c.transform.cmd)
    at = action_transform(c.transform.act)
    def full_action(line):
        true_line = ' '.join(line.split(' ')[1:])
        s = at(ct(lt(true_line)))
        # with open("C:\\Temp\\cho.out", "w") as f:
        #     f.write(s)
        # print(s)
        return s

    c.full_action = full_action
    c.read_path = c.get('read_path', 'C:\\Users\\tmasthay\\.basher\\.tmp\\no.out')
    return c

def clip(x, run=True):
    if '.ui' in x:
        cmd = f"echo {x} ^^^& | clip"
    else:
        cmd = f"echo {x} | clip"

    if run:
        cmd += ' && powershell -Command "My-Paste"'
    print(cmd)
    os.system(cmd)

def action_transform(transform_str):
    choices = {
        'clip': clip,
        'eval': lambda x : subprocess.check_output(x.split(' ')),
        'print': lambda x : print(x)
    }
    return choices[transform_str]

def command_transform(transform_str):
    choices = {
        'code': lambda x : f'code "{x}"',
        'vs': lambda x : f'des "{x}"' if x.endswith('.ui') else f'vs "{x}"',
        'raw': lambda x : x,
        None: lambda x : x
    }
    return choices.get(transform_str, lambda x : f'{transform_str} "{x}"')

def line_transform(transform_str):
    choices = {
        'id': lambda x : x,
        'rg': lambda x : x.split(':')[0],
        'rgc': lambda x : ':'.join(x.split(':')[:2])
    }
    return choices[transform_str]

@hydra.main(config_path="all/cho", config_name="default", version_base=None)
def main(cfg: DictConfig):
    c = preprocess_cfg(cfg)
    with open(c.read_path) as f:
        choices = f.read()
        # choices = strip_ansi_codes(choices)
        while '\n\n' in choices:
            choices = choices.replace('\n\n', '\n')
        while '  ' in choices:
            choices = choices.replace('  ', ' ')

        if len(choices.strip()) == 0:
            print('No results found.')
            return
       
        choices = choices.strip().split('\n')
       
        print('\n'.join(choices))
        if len(choices) == 1:
            choice = choices[0]
        else:
            response = input('Which line? ')
            if not response.isdigit():
                print('No action taken.')
                return
            choice = choices[int(response)]
        c.full_action(strip_ansi_codes(choice).strip())

if __name__ == "__main__":
    main()