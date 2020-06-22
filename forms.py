from flask_wtf import flask form
## prior to this, we ran pip install wtforms
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
## must import . validators to add as an argument later

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                    validators=[DataRequired(),Length(min=2,max=20)])
    ## allow usernames btw 2-20 characters
    ## make sure they're putting in some kind of input
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5,max=15)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=5, max=15), EqualTo('password')])

    submit = SubmitField('Sign Up')

class RegistrationForm(FlaskForm):
    email = StringField('Email', 
                    validators=[DataRequired(), Email())
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5,max=15)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')