import os

from flask import Flask, session, g,  render_template, flash, session, redirect, request, json
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import LoginForm, AddUserForm, AddQuestionForm
from models import db, connect_db, User, Question, Answer

CURR_USER_KEY = os.environ.get('CURR_USER_KEY', "current_user")

app = Flask(__name__)

# Get DB_URI from environ variable or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgres://postgres:pgwebdev@localhost:5432/quizby')


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)

##############################################################################
# User signup/login/logout


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


##############################################################################
# Login/Logout/Signup Routes

@app.route("/")
def home_dashboard():
    """Render Homepage based on user login status"""
    if g.user:
        return render_template('users/statistics.html')
    else:
        return render_template("home-quizby.html", page="home")


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = AddUserForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect('/')

    else:
        return render_template('users/signup.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()

    flash("You have successfully logged out.", "success")
    return redirect("/")

##############################################################################
# User Routes


@app.route('/users/<int:user_id>/quizzes')
def users_quizzes_dashboard(user_id):
    return render_template('users/quizzes.html')


@app.route('/users/<int:user_id>/questions')
def users_questions_dashboard(user_id):
    return render_template('users/questions.html')


##############################################################################
# Questions Routes

@app.route("/questions")
def questions():
    """ Page with listing of questions """

    search = request.args.get('q')

    if not search:
        questions = Question.query.all()
    else:
        questions = Question.query.filter(
            User.username.like(f"%{search}%")).all()
    return render_template('questions/questions.html', questions=questions)


@app.route("/questions/add", methods=["GET", "POST"])
def add_question():
    """ Add question form"""

    form = AddQuestionForm()

    if form.validate_on_submit():
        new_question = Question(
            question=form.question.data,
            mult_choice=form.mult_choice.data,
            category=form.category.data,
            user_id=g.user.id
        )
        db.session.add(new_question)
        db.session.commit()

        question = Question.query.filter_by(
            question=form.question.data).first()
        print(f"********************{question}")

        if form.mult_choice.data == True:
            answer_1 = Answer(
                answer=form.answer_one.data["answer"],
                correct=form.answer_one.data["correct"],
                question_id=question.id
            )
            answer_2 = Answer(
                answer=form.answer_two.data["answer"],
                correct=form.answer_two.data["correct"],
                question_id=question.id
            )
            answer_3 = Answer(
                answer=form.answer_three.data["answer"],
                correct=form.answer_three.data["correct"],
                question_id=question.id
            )
            answer_4 = Answer(
                answer=form.answer_four.data["answer"],
                correct=form.answer_four.data["correct"],
                question_id=question.id
            )

            db.session.add_all([
                new_question,
                answer_1,
                answer_2,
                answer_3,
                answer_4]
            )
        else:
            answer = Answer(
                answer=form.text_answer.data,
                correct=True,
                question_id=question.id
            )
            db.session.add(answer)

        db.session.commit()

        return redirect('/questions')
    else:
        return render_template('questions/add.html', form=form)
