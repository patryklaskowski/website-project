from website_project.main import HTML
from flask.testing import FlaskClient
import pytest


@pytest.mark.parametrize("name,expected_response", [
    ("", "<p>Welcome Stranger</p>"),
    ("python", "<p>Welcome Python</p>"),
    ("HolyGrail", "<p>Welcome Holygrail</p>"),
])
def test_welcome_page(flask_app: FlaskClient, name: str, expected_response: HTML):
    response = flask_app.get(f"/{name}")

    assert response.text == expected_response
    assert response.status_code == 200
