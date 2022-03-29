import pathlib
import yaml

base_dir = pathlib.Path(__file__).parent.parent.parent
config_path = base_dir / "config/pool.yaml"


def get_config(path):
    with open(path) as f:
        cfg = yaml.safe_load(f)
    return cfg


CONFIG = get_config(config_path)
