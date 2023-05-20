from flask.testing import FlaskClient


def test_welcome_page(flask_app: FlaskClient):
    response = flask_app.get()

    assert response.status_code == 200
    assert "<h1>Welcome to 'Website-Project'</h1>" in response.text

