from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from .models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is taken, its should be unique!')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log in')

class WordForm(FlaskForm):
    word = StringField('Word', validators=[DataRequired()])
    search = SubmitField('Search')

class WordInsert(FlaskForm):
    word = StringField('Word')
    definition = StringField('Definition')
    examples = StringField('Examples')
    insert = SubmitField('Insert Word')

class Practice(FlaskForm):
    text = StringField('Text')
    secret1 = StringField('Secret 1')
    secret2 = StringField('Secret 2')
    secret3 = StringField('Secret 3')
    button1 = SubmitField('Button1')
    button2 = SubmitField('Button2')
    button3 = SubmitField('Button3')