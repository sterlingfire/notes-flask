"""Flask app.py for notes app."""

from flask import Flask, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///adopt"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

@app.route("/")
def show_index():
    """ Redirects to /register. """
    return redirect("/register")


@app.route("/register")
def show_register_user_form():
    """ Shows a form that registers a user. """

    form = AddUserForm()

    if form.validate_on_submit():
        new_user = User.register(
            {
                "username":form.username.data,
                "password":form.password.data,
                "first_name":form.first_name.data,
                "last_name":form.last_name.data,
                "email":form.email.data,
            }
        )
    else:
        return render_template("register.html", form=form)
