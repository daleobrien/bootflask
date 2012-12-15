# -*- coding: utf-8 -*-
"""

"""

from flask import (Flask, request, render_template, redirect, url_for,
                   jsonify)
from flask.ext.login import (LoginManager, login_required,
                            login_user, logout_user,
                            fresh_login_required)

from models import User, Anonymous
from settings import USERS, MENUS, USER_NAMES


app = Flask(__name__)


app.config.from_object(__name__)

login_manager = LoginManager()

login_manager.anonymous_user = Anonymous
login_manager.login_view = "login"
#login_manager.login_message = u"Please log in to access this page."
login_manager.refresh_view = "reauth"


@login_manager.user_loader
def load_user(id):
    return USERS.get(int(id))


login_manager.setup_app(app)


@app.route("/")
@fresh_login_required
def index():
    return render_template("main.html")


@app.route("/_menu")
@fresh_login_required
def menu_route():

    menu_pick = request.args.get('id', 0, type=str)

    data = {}

    # figure out which panel, and load as needed
    if menu_pick in MENUS:
        for element, snippet in MENUS[menu_pick].items():
            data[element] = render_template(snippet)

    return jsonify(data)


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST" and "username" in request.form:

        username = request.form["username"]
        password = request.form["password"]

        if User.check_password(username, password):

            remember = request.form.get("remember", "no") == "yes"

            if login_user(USER_NAMES[username], remember=remember):

                return redirect(request.args.get("next") or url_for("index"))

    return render_template("main.html")


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run()
