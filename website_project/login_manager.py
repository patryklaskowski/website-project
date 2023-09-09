from typing import Optional
from flask import Flask
from flask_login import LoginManager

from website_project.user import GuestUser, User, find_user_by_username


def _load_user(username: str) -> Optional[User]:
    """Returns user associated with given username.

    Flask-login requires to define a “user_loader” function which,
    given a user ID, returns the associated user object.
    """
    return find_user_by_username(username)


def create_login_manager(flask_app: Flask) -> LoginManager:
    """Handles LoginManager setup."""
    assert flask_app.secret_key, "Secret key has to be configured."

    login_manager = LoginManager()
    login_manager.init_app(flask_app)

    login_manager.anonymous_user = GuestUser
    login_manager.user_loader(_load_user)

    return login_manager
