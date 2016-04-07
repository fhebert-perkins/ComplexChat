"""
Webclient Server application written in flask
"""

from flask import Flask, redirect, url_for, request, render_template, session
from models import db, User, Conversation

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(APP)
db.app = APP
db.create_all()

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
        try:
            assert request.form.get("email", None) is not None
            assert request.form.get("password", None) is not None
        except AssertionError:
            return render_template("login.html")
        if User.query.filter_by(email=request.form.get("email")).first().login(request.form.get("password")):
            session["logged_in"] = True
            return redirect(url_for("root"))
    else:
        return render_template("login.html")

@APP.route("/signup", methods=["POST", "GET"])
def signup():
    if session.get("logged_in", False) is True:
        return redirect(url_for("root"))
    if request.method == "POST":
        try:
            assert request.form.get("password", None) is not None
            assert request.form.get("email", None) is not None
            assert request.form.get("name", None) is not None
            assert request.form.get("password") == request.form.get("password1")
            assert request.form.get("email", None) is not None
        except AssertionError:
            return "Something was not input correctly"
        try:
            # Checks that there is no previous user with the provided email in the database
            assert User.query.filter_by(email=request.form.get("email")).first() is not True
            # checks that there is no previous user with the provided email in the database
            assert User.query.filter_by(username=request.form.get("username")).first() is not True
        except AssertionError:
            return "Username or email already in use"

        # If everything checks out add the user to the database
        User(request.form.get("username"), request.form.get("email"), request.form.get("password"))
    else:
        return render_template("signup.html")

if __name__ == "__main__":
    APP.run(debug=True)
