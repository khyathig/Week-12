from flask import Flask, render_template, request

app = Flask(__name__, template_folder="templates")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    username = request.form["username"]
    return f"Hello, {username}! Welcome to the website"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)