from typing import Optional

from flask import Flask, session, request, redirect, url_for, Response
from flask_login import LoginManager

from website_project.user import find_user_by_username, User, GuestUser
from website_project.common import Cookie, Alert, AlertType, html_anchor


def _unauthorized_access_view() -> Response:
    """Handles unauthorized situation.

    When guest user tries to access website for logged-in users only.

    Note:
        Remember, that not only website buttons direct to specific web page,
        is might also be typed in by hand. Guard against unauthorized access
        with this generic solver.
    """
    print(f"You need to be logged in to enter {url_for(request.endpoint)} endpoint.")
    session[Cookie.ALERT] = Alert(
        AlertType.WARNING,
        f"You need to be logged in to access {html_anchor(request.endpoint)} endpoint.",
    )

    session[Cookie.REDIRECT_BACK] = request.endpoint

    return redirect(url_for('auth.login'))


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
    login_manager.unauthorized_handler(_unauthorized_access_view)

    return login_manager
