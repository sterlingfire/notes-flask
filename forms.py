from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length
from email_validator import validate_email, EmailNotValidError


class AddUserForm(FlaskForm):
    """ User registration form. """
    username = StringField("Username",
                           validators=[InputRequired()])
    password = PasswordField("Password",
                             validators=[InputRequired()])
    first_name = StringField("First name",
                             validators=[InputRequired()])
    last_name = StringField("Last name",
                            validators=[InputRequired()])
    email = StringField("Email",
                        validators=[InputRequired(), Email()])


class LoginForm(FlaskForm):
    """ User login form. """
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class NoteForm(FlaskForm):
    """ Add new Note form. """
    title = StringField("Title",
                        validators=[InputRequired(), Length(max=100)])
    content = StringField("Content", validators=[InputRequired()])
