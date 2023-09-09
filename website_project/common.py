import re
import os
from typing import Dict, Optional
from dataclasses import dataclass

import yaml
from flask import url_for

ROOT_DIR: str = os.path.split(re.search(r'(^.+website_project)', __file__).group(1))[0]


def get_config() -> Dict:
    path = os.path.join(ROOT_DIR, "config.yml")
    with open(path, "r") as stream:
        return yaml.safe_load(stream)


class AlertType:
    """Provides available alert types for HTML content."""
    SUCCESS = "success"
    ERROR = "danger"
    INFO = "info"
    WARNING = "warning"


@dataclass
class Alert:
    """Support data type for html alerts."""
    type: AlertType
    msg: str


# TODO: unit test
def link_to(endpoint: str, text: Optional[str] = None) -> str:
    """Provides HTML link to given endpoint.

    Remember that when injecting in HTML through Jinja variable,
    it requires additional "safe" annotation to let it be actually
    treated as HTML element.
    """
    return f"<a href='{url_for(endpoint)}'>{text if text is not None else endpoint}</a>"
