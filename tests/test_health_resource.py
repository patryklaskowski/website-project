import pytest
from flask.testing import FlaskClient


def test_fail():
    assert False


@pytest.mark.parametrize("endpoint", ["/restapi/", "/restapi/health"])
def test_health_resource(flask_app: FlaskClient, endpoint: str):
    expected_response = {
        "message": "ok",
    }

    response = flask_app.get(endpoint)

    assert response.json == expected_response
    assert response.status_code == 200
