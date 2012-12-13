# -*- coding: utf-8 -*-
"""
Flask-Login example
===================
This is a small application that provides a trivial demonstration of
Flask-Login, including remember me functionality.

:copyright: (C) 2011 by Matthew Frazier.
:license:   MIT/X11, see LICENSE for more details.
"""
from flask import Flask, request, render_template, redirect, url_for, flash
from flask.ext.login import (LoginManager, login_required,
                            login_user, logout_user, UserMixin, AnonymousUser,
                            confirm_login, fresh_login_required)

from bcrypt import hashpw
import weakref


class User(UserMixin):

    instances = []

    def __init__(self, name, id, hashed_password, active=True):
        User.instances.append(weakref.proxy(self))
        self.name = name
        self.id = id
        self.active = active
        self.hashed_password = hashed_password

    def is_active(self):
        return self.active

    @classmethod
    def check_password(cls, user_name, password):

        for user in User.instances:
            if user.name == user_name:
                return hashpw(password, user.hashed_password) == \
                                                          user.hashed_password
        return False


class Anonymous(AnonymousUser):
    name = u"Anonymous"

# passwords generated like this
# hashpw("password", bcrypt.gensalt(14))
# where 14 is the work factor, the larger it is, the harder and slower it is.
USERS = {
    1: User(u"Notch", 1,
               '$2a$13$M9gsC/vjPTwUEFVTWO0Md./xnCcm.9ve55e3Y8cQ66Kw9fe9.5JXu'),
    2: User(u"Steve", 2,
               '$2a$13$OCggYrEukY0zdBM8tOuTUeUwP4KmgBa8KwIH/3dqzfJvSYqGBHdq2'),
    3: User(u"Creeper", 3,
        '$2a$14$9uCZINep37AT2u3bwgquF..NvWACbQ7Ra9ermgH3PYKMu5GmBfjjC', False),
}

USER_NAMES = dict((u.name, u) for u in USERS.itervalues())


app = Flask(__name__)

SECRET_KEY = "yeah, not actually a secret"
DEBUG = True

app.config.from_object(__name__)

login_manager = LoginManager()

login_manager.anonymous_user = Anonymous
login_manager.login_view = "login"
login_manager.login_message = u"Please log in to access this page."
login_manager.refresh_view = "reauth"


@login_manager.user_loader
def load_user(id):
    return USERS.get(int(id))


login_manager.setup_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/secret")
@fresh_login_required
def secret():
    return render_template("secret.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST" and "username" in request.form:
        username = request.form["username"]
        password = request.form["password"]
        if User.check_password(username, password):
            remember = request.form.get("remember", "no") == "yes"
            if login_user(USER_NAMES[username], remember=remember):
                flash("Logged in!")
                return redirect(request.args.get("next") or url_for("index"))
            else:
                flash("Sorry, but you could not log in.")
        else:
            flash(u"Invalid username or password.")
    return render_template("login.html")


@app.route("/reauth", methods=["GET", "POST"])
@login_required
def reauth():
    if request.method == "POST":
        confirm_login()
        flash(u"Reauthenticated.")
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("reauth.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run()
