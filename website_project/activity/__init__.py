from typing import Dict

from website_project.activity.swimming import read_swimming_data
from website_project.activity.running import read_running_data


def read_activity_specific_data(activity: str, data: Dict) -> Dict:
    mapping = {
        "swimming": read_swimming_data,
        "running": read_running_data,
    }
    return mapping[activity](data)
