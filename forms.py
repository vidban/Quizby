from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, IntegerField, SelectField
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


class AddQuestionsForm(FlaskForm):
    """ Form for adding questions."""

    question = StringField('Question', validators=[
                           DataRequired(), Length(max=200)]),
    mult_choice = BooleanField('Multiple choice?'),
    mult_choice_ans = SelectField('Answers', choices=[]),
    str_ans = StringField('Answer')
