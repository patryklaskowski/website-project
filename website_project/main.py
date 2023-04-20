import logging
from markupsafe import escape
from flask import Flask, request
from flask_restful import Resource, Api
from typing import NewType

app = Flask(__name__)
api = Api(app)

LOG = logging.getLogger(__name__)

API_PREFIX = "restapi"

HTML = NewType("html", str)
JSON = NewType("json", dict)


@app.route("/", methods=['GET'])
@app.route("/<name>", methods=['GET'])
def welcome_page(name="Stranger") -> HTML:
    LOG.info(f"{request.method} ")

    return f"<p>Welcome {escape(name.capitalize())}</p>"


class HealthResource(Resource):
    @staticmethod
    def get() -> JSON:
        return {"message": "ok"}


api.add_resource(
    HealthResource,
    f"/{API_PREFIX}/health",
    f"/{API_PREFIX}/")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
    )