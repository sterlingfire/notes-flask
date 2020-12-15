"""Flask app.py for notes app."""

from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import AddUserForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///notes"
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


@app.route("/register", methods=["GET", "POST"])
def register_user():
    """ GET - Shows a form that registers a user.
        POST - Creates new user in database
    """

    form = AddUserForm()

    if form.validate_on_submit():
        if User.query.get(form.username.data):
            flash("Username already exists. Please pick a new username.")
            return render_template("register.html", form=form)
        new_user = User.register(
            {
                "username": form.username.data,
                "password": form.password.data,
                "first_name": form.first_name.data,
                "last_name": form.last_name.data,
                "email": form.email.data,
            }
        )
        db.session.add(new_user)
        db.session.commit()
        session["user_id"] = form.username.data
        return redirect("/secret")
    else:
        return render_template("register.html", form=form, title="Register")


@app.route("/login", methods=["GET", "POST"])
def login_user():
    """ GET - Show login user form
        POST - Authenticate and then login in user via session cookie
    """

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(
            form.username.data,
            form.password.data,
        )
        if user:
            session["user_id"] = form.username.data
            return redirect("/secret")
        else:
            form.username.errors = ["Bad username/password"]

    return render_template("login.html", form=form, title="Login")


@app.route("/users/<username>")
def you_made_it(username):
    """ Secret user page  """

    if session["user_id"] == username:
        user = User.query.get_or_404(username)
        return render_template("user_details.html",
                              user=user,
                              title=f"Welcome {username}")
    return redirect('/login')


@app.route("/logout")
def logout_user():
    """ Logout user by clearing session info  """

    session.pop("user_id", None)

    flash("User was successfully logged out")
    return redirect("/")
