import hydra
from omegaconf import DictConfig
import os


@hydra.main(config_path="tpt_cfg", config_name="cfg", version_base=None)
def main(cfg: DictConfig) -> None:
    matches = []
    for k, v in cfg.alias.items():
        if cfg.t in v:
            matches.append(k)
    if len(matches) != 1:
        raise ValueError(
            f"Expected 1 match, got {len(matches)} matches in {matches}"
        )
    true_file = os.path.join(cfg.path, matches[0])
    if cfg.o is None:
        ext = matches[0].split('.')[-1]
        true_out = f'{cfg.t}.{ext}'
        if cfg.oldpwd:
            true_out = os.path.join(os.environ['OLDPWD'], true_out)
        else:
            true_out = os.path.join(os.getcwd(), true_out)
    else:
        true_out = cfg.o
    with open(true_file, 'r') as f:
        true_content = f.read()
    if cfg.o == 'stdout':
        print(true_content)
    else:
        if os.path.exists(true_out):
            raise FileExistsError(
                f"{true_out} already exists.\n"
                "If you wish to overwrite, use o=stdout and copy and paste."
            )
        else:
            with open(true_out, 'w') as f:
                f.write(true_content)
            print(f'Saved template {cfg.t} to {os.path.abspath(true_out)}')


if __name__ == "__main__":
    main()
