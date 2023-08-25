from website_project.common import get_config


def test_config_exists():
    assert get_config()
