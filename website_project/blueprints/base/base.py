from flask import Blueprint, render_template, session

from website_project.common import Cookie

base_bp = Blueprint(
    name='base',
    import_name=__name__,
    template_folder='templates',
    static_folder='static',
)


@base_bp.route("/", methods=['GET'])
def home_page() -> str:
    """Website home page."""
    return render_template("welcome.html", alert=session.pop(Cookie.ALERT, None))
