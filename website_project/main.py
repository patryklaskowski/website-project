from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=['GET'])
def home_page() -> str:
    return render_template("welcome.html")


@app.route("/activity", methods=['GET', 'POST'])
def activity_form() -> str:
    if request.method == 'GET':
        return render_template("activity_form.html")

    print(f"POST request form: `{request.form}`")
    return render_template("activity_form.html")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
    )
