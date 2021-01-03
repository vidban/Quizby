import os
import requests

from secrets import UNSPLASH_API_KEY, SECRET_KEY, CURR_USER_KEY, DATABASE_URL, UNSPLASH_API_URL

from flask import Flask, session, g,  render_template, flash, session, redirect, request, json
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import LoginForm, AddUserForm, AddQuestionForm, EditUserForm, CreateQuizForm
from models import db, connect_db, User, Question, Answer
from werkzeug.utils import secure_filename

CURR_USER_KEY = os.environ.get('CURR_USER_KEY', "current_user")

app = Flask(__name__)

# Get DB_URI from environ variable or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL or 'postgres:///quizby'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = SECRET_KEY or "it's a secret"
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
            )
            db.session.commit()

        except IntegrityError:
            flash("Username/Email already taken", 'danger')
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


@app.route('/users/profile')
def view_user_profile():
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/"
                        )
    user = g.user

    return render_template('/users/profile/view.html', user=user)


@app.route('/users/profile/edit', methods=["GET", "POST"])
def user_profile():
    """show/update user profile"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/"
                        )
    user = g.user
    form = EditUserForm(obj=user)

    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.email = form.email.data
            user.firstname = form.firstname.data
            user.lastname = form.lastname.data
            # If image file provided, save image data
            if form.image_url.data:
                f = form.image_url.data
                filename = secure_filename(f.filename)
                f.save('static/images/uploads/'+filename)
                user.image_url = f"/static/images/uploads/{filename}"

                flash('Image uploaded successfully', 'success')
            else:
                user.image_url = 'default-pic.png'
            db.session.commit()
            return redirect('/users/profile')

        flash("Wrong password, please try again.", 'danger')

    return render_template('users/profile/edit.html', form=form)


@app.route('/users/<int:user_id>/quizzes')
def users_quizzes_dashboard(user_id):
    """ get user's quizzes"""

    return render_template('users/quizzes.html')


@app.route('/users/<int:user_id>/questions')
def users_questions_dashboard(user_id):
    """ Get user's questions"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    questions = Question.query.filter(Question.user_id == g.user.id).all()
    return render_template('users/questions.html', questions=questions)


############################################################################
# Questions Routes

@ app.route("/questions")
def questions():
    """ Page with listing of questions """

    search = request.args.get('q')

    if not search:
        questions = Question.query.all()
    else:
        questions = Question.query.filter(
            Question.question.like(f"%{search}%")).all()
    return render_template('questions/questions.html', questions=questions)


@ app.route("/questions/add", methods=["GET", "POST"])
def add_question():
    """ Add question form"""

    if not g.user:
        flash("Please sign in to add questions", "danger")
        return redirect("/login")

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

        if form.mult_choice.data == True:
            if form.answer_one.data["answer"]:
                answer_1 = Answer(
                    answer=form.answer_one.data["answer"],
                    correct=form.answer_one.data["correct"],
                    question_id=question.id
                )
                db.session.add(answer_1)
            if form.answer_two.data["answer"]:
                answer_2 = Answer(
                    answer=form.answer_two.data["answer"],
                    correct=form.answer_two.data["correct"],
                    question_id=question.id
                )
                db.session.add(answer_2)
            if form.answer_three.data["answer"]:
                answer_3 = Answer(
                    answer=form.answer_three.data["answer"],
                    correct=form.answer_three.data["correct"],
                    question_id=question.id
                )
                db.session.add(answer_3)
            if form.answer_four.data["answer"]:
                answer_4 = Answer(
                    answer=form.answer_four.data["answer"],
                    correct=form.answer_four.data["correct"],
                    question_id=question.id
                )
                db.session.add(answer_4)
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


@ app.route('/questions/<int:question_id>/delete', methods=["POST"])
def delete_question(question_id):
    """ Delete a user's question """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    q = Question.query.get_or_404(question_id)

    db.session.delete(q)
    db.session.commit()

    flash("Question deleted", "success")

    return redirect(f"/users/{g.user.id}/questions")

############################################################################
# Quizzes Routes


@app.route('/create', methods=["GET", "POST"])
def create():
    """ Create a new quiz"""

    form = CreateQuizForm()

    return render_template("users/create.html", form=form)


############################################################################
# API Routes

@app.route('/search')
def search():
    """ render the image search modal for the API search for creating a quiz"""

    return render_template("users/search.html")


@app.route('/search/unsplash')
def search_unsplash():
    """Search the unsplash API for images"""

    if request.args:
        query = request.args["image-query"]
        res = requests.get(f"{UNSPLASH_API_URL}/search/photos/",
                           params={'client_id': UNSPLASH_API_KEY, "query": query, "w": "400"})
        data = res.json()
        images = []
        if len(data["results"]) > 12:
            for i in range(12):
                images.append([data["results"][i]["urls"]["thumb"], data["results"][i]
                               ["user"]["username"], data["results"][i]["links"]["self"]])
        else:
            for i in range(len(data["results"])):
                images.append([data["results"][i]["urls"]["thumb"], data["results"][i]
                               ["user"]["username"], data["results"][i]["links"]["self"]])

        return render_template("users/search.html", images=images)
    else:
        flash("Please enter a search term", "danger")
        return render_template("users/search.html")
