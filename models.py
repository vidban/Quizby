"""SQLAlchemy models for Quizby."""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    firstname = db.Column(
        db.Text,
    )

    lastname = db.Column(
        db.Text,
    )

    image_url = db.Column(
        db.Text,
        default="/static/images/default-pic.png",
    )

    level = db.Column(
        db.Integer,
    )

    points = db.Column(
        db.Integer,
    )

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

    @classmethod
    def signup(cls, username, email, password, image_url):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            image_url=image_url,
        )

        db.session.add(user)
        return user

    def __repr__(self):
        return f"<User {self.username} {self.email} {self.firstname} {self.lastname}>"


class Answer(db.Model):
    """Answers for available questions"""

    __tablename__ = "answers"

    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String)
    correct = db.Column(db.Boolean)
    question_id = db.Column(
        db.Integer,
        db.ForeignKey('questions.id'),
        nullable=False
    )
    question = db.relationship('Question', backref="answers")


class Question(db.Model):
    """Questions available"""

    __tablename__ = 'questions'

    id = db.Column(
        db.Integer,
        primary_key=True)

    question = db.Column(db.Text, unique=True)

    mult_choice = db.Column(db.Boolean)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )
    category = db.Column(db.Text())

    user = db.relationship('User', backref='questions')

    def __repr__(self):
        return f"<Question {self.question} {self.mult_choice} {self.user_id}>"


def connect_db(app):
    """Connect this database to provided Flask app."""

    db.app = app
    db.init_app(app)
