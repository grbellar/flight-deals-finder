from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired


class RegisterUserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class AddFlightTracking(FlaskForm):
    departure = StringField('Departing city', validators=[DataRequired()])
    destination = StringField('Destination', validators=[DataRequired()])
    price = IntegerField("Your desired price", validators=[DataRequired()])
    submit = SubmitField('Start tracking')
