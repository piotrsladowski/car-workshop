from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class NewJobButtonForm(FlaskForm):
    newJob = SubmitField('New job')

class procrastinationButtonForm(FlaskForm):
    procrastination = SubmitField('Procrastinate')

class ageNoButtonForm(FlaskForm):
    ageNo = SubmitField('No')

class ageYesButtonForm(FlaskForm):
    ageYes = SubmitField('Yes')


class IndexForm(FlaskForm):
    car = StringField('Car', validators=[DataRequired()])
    submit = SubmitField('Submit')
