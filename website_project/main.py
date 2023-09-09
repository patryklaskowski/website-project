from dataclasses import dataclass
from typing import List
from datetime import timedelta

from dotenv import load_dotenv
from flask import Response, Flask, render_template, request, redirect, url_for, session
from flask_login import current_user, login_required, login_user, logout_user

from website_project.activity import read_activity_specific_data, activities
from website_project.common import get_config, Alert, AlertType, link_to
from website_project.database.driver import MongoDb
from website_project.login_manager import create_login_manager
from website_project.user import (
    RegisteredUser,
    find_user_by_username,
    register_user,
    user_exists,
)

load_dotenv()

config = get_config()
db = MongoDb(
    db_name=config["mongodb"]["db_name"],
    username=config["mongodb"]["username"],
)


class Cookie:
    """Support for session values."""
    ALERT = "my_alert"
    REDIRECT_BACK = "my_redirect_back"


def create_app() -> Flask:
    """Handles Flask setup."""
    flask_app = Flask(__name__)
    flask_app.secret_key = "secret"

    return flask_app


app = create_app()
login_manager = create_login_manager(app)


@login_manager.unauthorized_handler
def unauthorized_access_view() -> Response:
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
        f"You need to be logged in to access {link_to(request.endpoint)} endpoint.",
    )

    session[Cookie.REDIRECT_BACK] = request.endpoint

    return redirect(url_for('login'))


@dataclass
class DataTable:
    """Support data type to construct html table elements."""
    activity: str
    columns: List[str]
    rows: List[List[str]]


# TODO: This is either queried all at once by selected activity
def get_all_data() -> List[DataTable]:
    """Retrieves all data for all activities."""
    all_data = []
    for activity in activities:
        df = db.read_all(activity.name, activity.schema)
        all_data.append(DataTable(
            activity=activity.name,
            columns=df.columns.to_list(),
            rows=df.values,
        ))

    return all_data


@app.route('/login', methods=["POST", "GET"])
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

            return redirect(url_for('login'))

        print(f"Login successful for {user}")
        session[Cookie.ALERT] = Alert(AlertType.INFO, f"Successful login, {user.username}")
        login_user(user, remember=True, duration=timedelta(weeks=1))

        if session.get(Cookie.REDIRECT_BACK, None):
            return redirect(url_for(session.pop(Cookie.REDIRECT_BACK)))

        return redirect(url_for('profile'))


@app.route('/signup', methods=["POST", "GET"])
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

        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        session[Cookie.ALERT] = Alert(AlertType.INFO, f"User logged out.")

    return redirect(url_for('login'))


@app.route('/profile')
def profile():
    return render_template(
        'profile.html',
        alert=session.pop(Cookie.ALERT, None),
        name=current_user.username
    )


@app.route("/", methods=['GET'])
def home_page() -> str:
    """Website home page."""
    return render_template("welcome.html", alert=session.pop(Cookie.ALERT, None))


@app.route("/activity", methods=['GET', 'POST'])
@login_required
def activity_form() -> str:
    """Provides activity form api to add new activity record.

    On GET request form is provided.
    On POST request form data is parsed according to selected activity,
        and saved in database.
    """
    if request.method == "GET":
        return render_template("activity_form.html", alert=session.pop(Cookie.ALERT, None))
    elif request.method == "POST":
        form_data = request.form.to_dict()
        print(f"POST request form: `{form_data}`")

        try:
            activity = form_data["activity"]

            activity_data = read_activity_specific_data(activity, form_data)
            db.save_record(collection_name=activity, data=activity_data)

            alert = Alert(AlertType.SUCCESS, "Record added successfully.")
        except Exception as e:
            alert = Alert(AlertType.ERROR, f"Excpetion occured: `{e}`")

        return render_template("activity_form.html", alert=alert)


@app.route("/data", methods=['GET'])
@login_required
def activity_data() -> str:
    """Present registered activity data."""
    return render_template("activity_data.html", all_data=get_all_data(), alert=session.pop(Cookie.ALERT, None))


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        threaded=True,
    )
