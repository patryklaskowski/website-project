from website_project.main import create_app
import pytest
from flask.testing import FlaskClient

app = create_app()


@pytest.fixture
def flask_app() -> FlaskClient:
    # Executed for each test case
    with app.test_client() as test_client:
        yield test_client
