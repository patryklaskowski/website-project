"""
Provides pages:

- login
- logout
- signup
- profile
"""

from datetime import timedelta

from flask import Blueprint, render_template, session, request, redirect, url_for
from flask_login import login_user, current_user, logout_user

from website_project.user import find_user_by_username, RegisteredUser, user_exists, register_user
from website_project.common import Cookie, Alert, AlertType

auth_bp = Blueprint(
    name='auth',
    import_name=__name__,
    template_folder='templates',
    static_folder='static',
)


@auth_bp.route('/login', methods=["POST", "GET"])
def login():
    """Login page."""
    if request.method == "GET":
        return render_template("login.html", alert=session.pop(Cookie.ALERT, None))
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = find_user_by_username(username)
        if not user or not user.has_password(password):
            print("Login failed, provided invalid username or password.")
            session[Cookie.ALERT] = Alert(AlertType.ERROR, f"Invalid username or password.")

            return redirect(url_for('auth.login'))

        print(f"Login successful for {user}")
        session[Cookie.ALERT] = Alert(AlertType.INFO, f"Successfuly logged in as {user.username} user")
        login_user(user, remember=True, duration=timedelta(weeks=1))

        if session.get(Cookie.REDIRECT_BACK, None):
            return redirect(url_for(session.pop(Cookie.REDIRECT_BACK)))

        return redirect(url_for('auth.profile'))


@auth_bp.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == "GET":
        return render_template("signup.html", alert=session.pop(Cookie.ALERT, None))
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = RegisteredUser(username, password)

        if user_exists(user):
            return render_template(
                "signup.html",
                alert=Alert(
                    AlertType.ERROR,
                    f"Username `{user.username}` already in use.",
                )
            )

        register_user(user)
        print(f"Registered new user: {user.username}")
        session[Cookie.ALERT] = Alert(AlertType.SUCCESS, f"New user has been created: {user.username}")

        if not current_user.is_authenticated:
            login_user(user, remember=True, duration=timedelta(weeks=1))

        return redirect(url_for('auth.profile'))


@auth_bp.route('/logout', methods=["GET"])
def logout():
    if current_user.is_authenticated:
        session[Cookie.ALERT] = Alert(AlertType.INFO, f"Bye bye {current_user.username}.")
        logout_user()

    return redirect(url_for('auth.login'))


@auth_bp.route('/profile')
def profile():
    return render_template(
        'profile.html',
        alert=session.pop(Cookie.ALERT, None),
        name=current_user.username
    )
