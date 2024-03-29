from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, IntegerField, SelectField, FieldList, FormField, FileField, RadioField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.file import FileAllowed


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


class EditUserForm(FlaskForm):
    """ Form for editing a user"""

    username = StringField('Username', validators=[
                           DataRequired()], render_kw={'autofocus': True})
    firstname = StringField('First Name')
    lastname = StringField('Last Name')
    image_url = FileField('image', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])


class AnswerForm(FlaskForm):
    """Form for adding answer options with correct choice option"""
    answer = StringField(id='answer')
    correct = BooleanField('Correct?', default=False)


class AddQuestionForm(FlaskForm):
    """ Form for adding questions."""
    category = StringField('Category', validators=[
        DataRequired()], description="Enter Category here", id="autocomplete")
    question = TextAreaField('Question', validators=[
        DataRequired(), Length(max=200)])
    mult_choice = RadioField('Question Type:', choices=[(
        'mc', 'Multiple Choice')], default='mc')
    answer_one = FormField(AnswerForm)
    answer_two = FormField(AnswerForm)
    answer_three = FormField(AnswerForm)
    answer_four = FormField(AnswerForm)
    text_answer = TextAreaField(
        'Answer', description='Enter the answer here...')
