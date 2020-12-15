"""Models for notes app."""
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """Connects this database to app.py
    Called by app.py (Flask app).
    """

    db.app = app
    db.init_app(app)


class User(db.Model):
    """ User class for auth & storage. """

    __tablename__ = "users"

    username = db.Column(db.String(20),
                         primary_key=True)
    password = db.Column(db.Text,
                         nullable=False)
    email = db.Column(db.String(50),
                      unique=True,
                      nullable=False)
    first_name = db.Column(db.String(30),
                           nullable=False)
    last_name = db.Column(db.String(30),
                          nullable=False)
    notes = db.relationship("Note", backref="user")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def serialize(self):
        """ Return serialized user """
        return {
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }

    @classmethod
    def register(cls, user_data):
        """ Register user with hashed password and return user. """

        hashed = bcrypt.generate_password_hash(user_data["password"]).decode("utf8")
        return cls(username=user_data["username"],
                   password=hashed,
                   first_name=user_data["first_name"],
                   last_name=user_data["last_name"],
                   email=user_data["email"])

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        db_user = User.query.filter_by(username=username).first()
        if db_user and bcrypt.check_password_hash(db_user.password, pwd):
            return db_user
        else:
            return False


class Note(db.Model):
    """ Note class for db access. """
    __tablename__ = "notes"
    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True)
    title = db.Column(db.String(100),
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    owner = db.Column(db.String(20),
                      db.ForeignKey("users.username"),
                      nullable=False)
