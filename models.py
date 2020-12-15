"""Models for notes app."""
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
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

    def serialize():
        """ Return serialized user """
        return {"username":self.username,
                "first_name":first_name,
                "last_name":last_name,
                "email":email}


    @classmethod
    def register(cls, user_data):
        """ Register user with hashed password and return user. """

        hashed = bcrypt.generate_password_hash(user_data["password"]).decode("utf8")
        return (cls(username=user,
                    password=hashed,
                    first_name=user_data["first_name"],
                    last_name=user_data["last_name"],
                    email=user_data["email"]))


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
