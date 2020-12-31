from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, IntegerField, SelectField, FormField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[
                           DataRequired()], render_kw={'autofocus': True})
    password = PasswordField('Password', validators=[Length(min=6)])


class AddUserForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[
                           DataRequired()], render_kw={'autofocus': True})
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')


class AnswerForm(FlaskForm):
    """Form for adding answer options with correct choice option"""
    answer = StringField('Answer')
    correct = BooleanField('Correct')


class AddQuestionForm(FlaskForm):
    """ Form for adding questions."""

    question = TextAreaField('Question', validators=[
                             DataRequired(), Length(max=200)])
    mult_choice = BooleanField('Multiple choice?')
    answer_one = FormField(AnswerForm)
    answer_two = FormField(AnswerForm)
    answer_three = FormField(AnswerForm)
    answer_four = FormField(AnswerForm)
    text_answer = TextAreaField('Answer')
    category = StringField('Category', validators=[DataRequired()])
