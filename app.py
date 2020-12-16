"""Flask app.py for notes app."""

from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Note
from forms import AddUserForm, LoginForm, NoteForm

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
        return redirect(f"/users/{new_user.username}")
    else:
        return render_template("register.html", form=form)


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
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Bad username/password"]

    return render_template("login.html", form=form)


@app.route("/users/<username>")
def show_user_details(username):
    """ Authenticated user page  """

    if session["user_id"] == username:
        user = User.query.get_or_404(username)
        return render_template("user_details.html",
                              user=user)
    return redirect('/login')


@app.route("/logout")
def logout_user():
    """ Logout user by clearing session info  """

    session.pop("user_id", None)

    flash("User was successfully logged out")
    return redirect("/")


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """ Delete a user from the database
        Delete all notes for user and clear the session
     """

    user_notes = Note.query.filter_by(owner=username)
    user_notes.delete()
    User.query.filter_by(username=username).delete()
    db.session.commit()

    session.pop("user_id", None)

    flash(f"User: {username} has been deleted.")
    return redirect("/")


@app.route("/users/<username>/notes/add")
def add_note(username):
    """ Add a note for the logged in user
        redirect to users/<username>
    """
    form = NoteForm()
    user = User.get_or_404(username)
    if form.validate_on_submit():
        new_note = Note(owner=username,
                        title=form.title.data,
                        content=form.content.data)
        user.notes.append(new_note)
        db.session.commit()
        return redirect (f"/users/{username}")
    return render_template("add_note.html", form=form)


@app.route("/notes/<int:note_id>/update", methods=["GET", "POST"])
def update_note(note_id):
    """ Update note by noteid.
    """
    note = Note.query.get_or_404(note_id)
    form = NoteForm()
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        db.session.commit()
        return redirect(f"/users/{note.owner}")
    return render_template("edit_note.html", form=form)


@app.route("/notes/<int:note_id>/update", methods=["POST"])
def delete_note(note_id):
    """ Deletes a note.
    """
    note = Note.query.get_or_404(note_id)
    username = note.owner
    db.session.delete(note)
    return redirect(f"/users/{username}")
