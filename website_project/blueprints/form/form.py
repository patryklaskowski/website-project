from dataclasses import dataclass
from typing import List

from flask import Blueprint, render_template, session, request
from flask_login import login_required

from website_project.activity import read_activity_specific_data, activities
from website_project.common import Cookie, Alert, AlertType, get_config
from website_project.database.driver import MongoDb

form_bp = Blueprint(
    name='form',
    import_name=__name__,
    template_folder='templates',
    static_folder='static',
)

config = get_config()
db = MongoDb(
    db_name=config["mongodb"]["db_name"],
    username=config["mongodb"]["username"],
)


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


@form_bp.route("/activity", methods=['GET', 'POST'])
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



@form_bp.route("/data", methods=['GET'])
@login_required
def activity_data() -> str:
    """Present registered activity data."""
    return render_template("activity_data.html", all_data=get_all_data(), alert=session.pop(Cookie.ALERT, None))
