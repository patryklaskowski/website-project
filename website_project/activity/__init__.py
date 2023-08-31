from typing import Dict

from website_project.activity import swimming
from website_project.activity import running


def read_activity_specific_data(activity: str, data: Dict) -> Dict:
    mapping = {
        swimming.name: swimming.read_swimming_data,
        running.name: running.read_running_data,
    }
    return mapping[activity](data)


activities = [swimming, running]
