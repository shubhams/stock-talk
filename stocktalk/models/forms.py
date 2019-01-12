from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length, EqualTo


class RegForm(FlaskForm):
	username = StringField('username', validators=[InputRequired(), Length(max=30)])
	password = PasswordField('password', validators=[InputRequired(),
	                                                 EqualTo('confirm_password', message='Passwords must match'),
	                                                 Length(min=8, max=30)])
	confirm_password = PasswordField('Repeat Password')


class LoginForm(FlaskForm):
	username = StringField('username', validators=[InputRequired(), Length(max=30)])
	password = PasswordField('password', validators=[InputRequired(),
	                                                 Length(min=8, max=30)])
	remember = BooleanField('remember')