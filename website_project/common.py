from typing import Dict
import yaml
import re
import os

ROOT_DIR: str = os.path.split(re.search(r'(^.+website_project)', __file__).group(1))[0]


def get_config() -> Dict:
    path = os.path.join(ROOT_DIR, "config.yml")
    with open(path, "r") as stream:
        return yaml.safe_load(stream)
