from dataclasses import dataclass

from dotenv import load_dotenv
from flask import Flask, render_template, request

from website_project.activity import read_activity_specific_data
from website_project.common import get_config
from website_project.database.driver import MongoDatabase

load_dotenv()

CONFIG = get_config()
app = Flask(__name__)
db = MongoDatabase()


@dataclass
class Alert:
    type: str
    msg: str


@app.route("/", methods=['GET'])
def home_page() -> str:
    return render_template("welcome.html")


@app.route("/activity", methods=['GET', 'POST'])
def activity_form() -> str:
    if request.method == 'GET':
        return render_template("activity_form.html")

    form_data = request.form.to_dict()
    print(f"POST request form: `{form_data}`")

    activity = form_data["activity"]

    activity_data = read_activity_specific_data(activity, form_data)
    db.save_record(collection_name=activity, data=activity_data)

    return render_template("activity_form.html", alert=Alert("success", "Record added successfully"))


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
    )
