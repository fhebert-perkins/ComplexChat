"""
Webclient Server application written in flask
"""

from flask import Flask, redirect, url_for, request, render_template, session


APP = Flask(__name__)

@APP.route("/")
def root():
    """Default action, return the webclient if the user is logged in"""
    if session.get("logged_in", False) is False:
        return redirect(url_for("login"))
    else:
        return render_template("webclient.html")

@APP.route("/login", methods=["POST", "GET"])
def login():
    """Login user"""
    if session.get("logged_in", False) is True:
        return redirect(url_for("root"))

    if request.method == "POST":
        return str(request.form)
        # Do the login Thing
    else:
        return render_template("login.html")

@APP.route("/signup", methods=["POST", "GET"])
def signup():
    if session.get("logged_in", False) is True:
        return render_template("signup.html")
    if request.method == "POST":
        return str(request.form)
    else:
        return render_template("signup.html")

if __name__ == "__main__":
    APP.run(debug=True)
