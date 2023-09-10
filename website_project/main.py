from dataclasses import dataclass
from typing import List

from dotenv import load_dotenv
from flask import Flask, render_template, request, session
from flask_login import login_required

from website_project.activity import read_activity_specific_data, activities
from website_project.common import get_config, Alert, AlertType, Cookie
from website_project.database.driver import MongoDb
from website_project.blueprints.auth import auth, create_login_manager

load_dotenv()

config = get_config()
db = MongoDb(
    db_name=config["mongodb"]["db_name"],
    username=config["mongodb"]["username"],
)


def create_app() -> Flask:
    """Handles Flask setup."""
    flask_app = Flask(__name__)
    flask_app.secret_key = "secret"

    flask_app.register_blueprint(auth)

    return flask_app


app = create_app()
login_manager = create_login_manager(app)


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
