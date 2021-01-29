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

    date_joined = db.Column(db.DateTime(timezone=False), nullable=False,
                            default=datetime.utcnow())

    favorites = db.relationship(
        'Question',
        secondary='favorites')

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
    def signup(cls, username, email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user

    def __repr__(self):
        return f"<User {self.username} {self.email}>"


class Answer(db.Model):
    """Answers for available questions"""

    __tablename__ = "answers"

    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String)
    correct = db.Column(db.Boolean)
    question_id = db.Column(
        db.Integer,
        db.ForeignKey('questions.id', ondelete='CASCADE'),
        nullable=False
    )


class Favorites(db.Model):

    __tablename__ = "favorites"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='cascade'))
    question_id = db.Column(db.Integer, db.ForeignKey(
        'questions.id', ondelete='cascade'))


class QuizQuestion(db.Model):
    """ relational table for quiz and questions"""

    __tablename__ = "quizzes_questions"

    quiz_id = db.Column(db.Integer, db.ForeignKey(
        'quizzes.id', ondelete="cascade"), primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey(
        'questions.id', ondelete="cascade"), primary_key=True)


class Question(db.Model):
    """Questions available"""

    __tablename__ = 'questions'

    id = db.Column(
        db.Integer,
        primary_key=True)

    question = db.Column(db.Text, unique=True)

    mult_choice = db.Column(db.String)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )
    category = db.Column(db.Text())
    private = db.Column(db.Boolean, default=True)
    favorite = db.Column(db.Boolean, default=False)
    created_on = db.Column(db.DateTime(timezone=False), nullable=False,
                           default=datetime.utcnow())
    correct = db.Column(db.Boolean, default=True)
    marked = db.Column(db.String)

    user = db.relationship('User', backref='questions')
    answers = db.relationship(
        'Answer', backref="question", cascade="all,delete")

    def __repr__(self):
        return f"<Question {self.question} {self.mult_choice} {self.user_id}>"


class Quiz(db.Model):
    """Quizzes available"""

    __tablename__ = 'quizzes'

    id = db.Column(
        db.Integer,
        primary_key=True)

    title = db.Column(db.Text)

    desc = db.Column(db.String)

    image_by = db.Column(db.String)

    image_by_profile = db.Column(db.String)
    image_desc = db.Column(db.String)
    image_url = db.Column(db.String)
    mult_choice = db.Column(db.String)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )
    category = db.Column(db.Text)
    private = db.Column(db.Boolean, default=True)
    created_on = db.Column(db.DateTime(timezone=False), nullable=False,
                           default=datetime.utcnow())

    user = db.relationship('User', backref='quizzes')

    questions = db.relationship(
        'Question', secondary='quizzes_questions')


class Category(db.Model):
    """ Categories Available """

    __tablename__ = "categories"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    name = db.Column(
        db.String,
        nullable=False,
        unique=True)

    def get_name(self):
        return self.name


def add_category(category):
    """ add new category to categories table when question or quiz is added"""
    ct = Category.query.filter(Category.name.ilike(category)).all()

    if len(ct) == 0:
        c = Category(name=category)

        db.session.add(c)
        db.session.commit()


def create_answer_sheet(quiz):
    """ create an answer sheet for given quiz"""

    ans_sheet = {}
    for question in quiz.questions:
        for answer in question.answers:
            if answer.correct:
                ans_sheet[question.id] = answer.answer

    return ans_sheet


def connect_db(app):
    """Connect this database to provided Flask app."""

    db.app = app
    db.init_app(app)
