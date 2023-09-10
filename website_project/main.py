from flask import Flask

from website_project.blueprints.auth import create_login_manager
from website_project.blueprints import form_bp, auth_bp, base_bp


def create_app() -> Flask:
    """Handles Flask setup."""
    flask_app = Flask(__name__)
    flask_app.secret_key = "secret"

    flask_app.register_blueprint(base_bp)
    flask_app.register_blueprint(auth_bp)
    flask_app.register_blueprint(form_bp)

    _ = create_login_manager(flask_app)

    return flask_app


if __name__ == "__main__":
    app = create_app()

    app.run(
        host="0.0.0.0",
        port=5000,
        threaded=True,
    )
