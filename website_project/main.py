from dataclasses import dataclass
from typing import List

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

from website_project.activity import read_activity_specific_data, activities
from website_project.common import get_config
from website_project.database.driver import MongoDb
from website_project.models import User, registered_users

load_dotenv()

config = get_config()
db = MongoDb(
    db_name=config["mongodb"]["db_name"],
    username=config["mongodb"]["username"],
)

from flask_login.mixins import AnonymousUserMixin
class Anonymous(AnonymousUserMixin):
  def __init__(self):
    self.name = 'Guest'



app = Flask(__name__)
app.secret_key = "secret"
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)
login_manager.anonymous_user = Anonymous

registered_users.append(User("root@gmail.com", generate_password_hash("root", "sha256"), "root"))

@login_manager.user_loader
def load_user(user_id):
    user = None
    if registered_users:
        for u in registered_users:
            if u.id == user_id:
                user = u
    return user


@dataclass
class Alert:
    """Support data type for html alerts."""
    type: str
    msg: str


class AlertType:
    SUCCESS = "success"
    ERROR = "danger"
    INFO = "info"


@dataclass
class DataTable:
    """Support data type to construct html table elements."""
    activity: str
    columns: List[str]
    rows: List[List[str]]


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
    if request.method == "GET":
        return render_template("login.html", alert=session.pop("alert", None))
    elif request.method == "POST":
        form = request.form

        user = None
        for u in registered_users:
            user = u if form["email"] == u.email else None

        if not user or not check_password_hash(user.password, form["password"]):
            session["alert"] = Alert(AlertType.ERROR, f"Invalid username or password.")
            return redirect(url_for('login'))

        session["alert"] = Alert(AlertType.INFO, f"Welcome, {user.name}")
        login_user(user)
        return redirect(url_for('profile'))


@app.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == "GET":
        return render_template("signup.html", alert=session.pop("alert", None))
    elif request.method == "POST":
        form = request.form

        user = User(
            email=form["email"],
            password=generate_password_hash(form["password"], method="sha256"),
            name=form["name"],
        )

        # Check if user already exists
        if user.email in [u.email for u in registered_users]:
            return render_template(
                "signup.html",
                alert=Alert(
                    AlertType.ERROR,
                    f"There's account connected to provided email: `{user.email}`.",
                )
            )

        # Add user
        registered_users.append(user)
        print(f"Registered new user: {user}")
        session["alert"] = Alert(AlertType.SUCCESS, f"User has been created with email: `{user.email}`")

        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    logout_user()
    session["alert"] = Alert(AlertType.INFO, f"User logged out.")
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    # alert = session.pop("alert") if "alert" in session else None
    return render_template('profile.html', alert=session.pop("alert", None), name=current_user.name)


@app.route("/", methods=['GET'])
def home_page() -> str:
    """Website home page."""
    # alert = session.pop("alert") if "alert" in session else None
    return render_template("welcome.html", alert=session.pop("alert", None))


@app.route("/activity", methods=['GET', 'POST'])
@login_required
def activity_form() -> str:
    """Provides activity form api to add new activity record.

    On GET request form is provided.
    On POST request form data is parsed according to selected activity,
        and saved in database.
    """
    if request.method == "GET":
        return render_template("activity_form.html")
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
    return render_template("activity_data.html", all_data=get_all_data())


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
    )
