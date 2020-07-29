from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, FloatField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    City = StringField('City',
                        validators=[DataRequired(),Length(min=2, max=20)])
    State = StringField('State',
                        validators=[DataRequired(),Length(min=2, max=20)])
    Zip = StringField('Zip',
                        validators=[DataRequired(),Length(min=5, max=5)])
    Company = StringField('Company',
                        validators=[DataRequired(),Length(min=4, max=100)])
    Department = StringField('Department',
                        validators=[DataRequired(),Length(min=4, max=100)])
    Title = StringField('Title',
                        validators=[DataRequired(),Length(min=4, max=100)])

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class PredictForm(FlaskForm):
    s_roeinjr = SelectField(choices = [("", "---"), ('1', '+'), ('2', '-')],validators=[DataRequired()])
    s_noijy = SelectField(choices = [("", "---"), ('1', '+'), ('2', '-')],validators=[DataRequired()])
    s_asset = SelectField(choices = [("", "---"), ('1', '+'), ('2', '-')],validators=[DataRequired()])
    s_RBCT1J = SelectField(choices = [("", "---"), ('1', '+'), ('2', '-')],validators=[DataRequired()])
    s_core_deposit = SelectField(choices = [("", "---"), ('1', '+'), ('2', '-')],validators=[DataRequired()])
    s_lnlsntv = SelectField(choices = [("", "---"), ('1', '+'), ('2', '-')],validators=[DataRequired()])
    s_County_GDP_Percent = SelectField(choices = [("", "---"), ('1', '+'), ('2', '-')],validators=[DataRequired()])
    s_PC_Labor_Force = SelectField(choices = [("", "---"), ('1', '+'), ('2', '-')],validators=[DataRequired()])
    s_PC_Unemployed = SelectField(choices = [("", "---"), ('1', '+'), ('2', '-')],validators=[DataRequired()])
    s_GR_Total_Population = SelectField(choices = [("", "---"), ('1', '+'), ('2', '-')],validators=[DataRequired()])
  
    roeinjr =  FloatField('Retained earnings to average equity (ytd only) (% change)',validators=[DataRequired(message=u"Please input percentage change"), NumberRange(min=0, max=100, message=u"Please input percentage change between 0 and 1")])
    noijy =  FloatField('Net operating income to assets (% change)',validators=[DataRequired(message=u"Please input percentage change"), NumberRange(min=0, max=100, message=u"Please input percentage change between 0 and 1")])
    asset =  FloatField('Total assets (% change)',validators=[DataRequired(message=u"Please input percentage change"), NumberRange(min=0, max=100, message=u"Please input percentage change between 0 and 1")])
    RBCT1J =  FloatField('Tier one (core) capital (% change)',validators=[DataRequired(message=u"Please input percentage change"), NumberRange(min=0, max=100, message=u"Please input percentage change between 0 and 1")])
    core_deposit =  FloatField('Core deposit (% change)',validators=[DataRequired(message=u"Please input percentage change"), NumberRange(min=0, max=100, message=u"Please input percentage change between 0 and 1")])
    lnlsntv =  FloatField('Net loans and leases to total asssets (% change)',validators=[DataRequired(message=u"Please input percentage change"), NumberRange(min=0, max=100, message=u"Please input percentage change between 0 and 1")])
    County_GDP_Percent =  FloatField('County GDP Percent (% change)',validators=[DataRequired(message=u"Please input percentage change"), NumberRange(min=0, max=100, message=u"Please input percentage change between 0 and 1")])
    PC_Labor_Force =  FloatField('Labor Force Percent (% change)',validators=[DataRequired(message=u"Please input percentage change"), NumberRange(min=0, max=100, message=u"Please input percentage change between 0 and 1")])
    PC_Unemployed =  FloatField('Unemployed Percent (% change)',validators=[DataRequired(message=u"Please input percentage change"), NumberRange(min=0, max=100, message=u"Please input percentage change between 0 and 1")])
    GR_Total_Population =  FloatField('GR Total Population (% change)',validators=[DataRequired(message=u"Please input percentage change"), NumberRange(min=0, max=100, message=u"Please input percentage change between 0 and 1")])
  
    Predict = SubmitField('Predict Bank Valuation')