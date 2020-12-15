from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.widgets import PasswordField
from wtforms.validators import InputRequired, Email


class AddUserForm():
    """ User registration form. """
    username = StringField("Username",
                            validators=[InputRequired()])
    password = StringField("Password",
                            widget=PasswordInput(hide_value=True),
                            validators=[InputRequired()])
    first_name = StringField("First name",
                            validators=[InputRequired()])
    last_name = StringField("Last name",
                            validators=[InputRequired()])
    email = StringField("Email",
                        validators=[InputRequired(), Email()])

class LoginForm():
    """ User login form. """
    username = StringField("Username",
                            validators=[InputRequired()])
    password = StringField("Password",
                            widget=PasswordInput(hide_value=True),
                            validators=[InputRequired()])
