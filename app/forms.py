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
    # States = SelectField(u'States name', choices=[["Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California", "Colorado", "Connecticut", "District ", "of Columbia", "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]])
    
    eqtot = IntegerField('Total equity capital',validators=[DataRequired(message=u"Please input integer number"), NumberRange(min=0, max=100000, message=u"Number is requred")])
    eq = IntegerField('Bank equity capital',validators=[DataRequired(message=u"Please input integer number"), NumberRange(min=0, max=100000, message=u"Number is requred")])
    IDP3REDM = IntegerField('Real estate loans in domestic offices, past due 30 - 89 days',validators=[DataRequired(message=u"Please input integer number"), NumberRange(min=0, max=100000, message=u"Number is requred")])
    IDNAREDM = IntegerField('Real estate loans in domestic offices in nonaccrual status',validators=[DataRequired(message=u"Please input integer number"), NumberRange(min=0, max=100000, message="Number is requred")])
    RBCT1J = FloatField('Tier one (core) capital',validators=[DataRequired(message=u"Please input integer number"), NumberRange(min=0, max=100000, message="Number is requred")])
    liabeq = FloatField('Total liabilities and capital',validators=[DataRequired(message=u"Please input integer number"), NumberRange(min=0, max=100000, message="Number is requred")])
    Lnrenr2N = FloatField('Number of loans sec. by nonfarm nonres. props. - orig. amts. $100K- $250K',validators=[DataRequired(message=u"Please input integer number"), NumberRange(min=0, max=100000, message="Number is requred")])
    crcon = FloatField('Loans to individuals',validators=[DataRequired(message=u"Please input integer number"), NumberRange(min=0, max=100000, message="Number is requred")])
    crci = FloatField('Commercial and industrial loans',validators=[DataRequired(message=u"Please input integer number"), NumberRange(min=0, max=100000, message="Number is requred")])
    Lnag1 = FloatField('$ amt. loans to finance agricultural prod. - orig. amts. of $100K or less',validators=[DataRequired(message=u"Please input integer number"), NumberRange(min=0, max=100000, message="Number is requred")])
    intexpy = FloatField('Cost of funding earning assets',validators=[DataRequired(message=u"Please input integer number"), NumberRange(min=0, max=100000, message="Number is requred")])
    esal= FloatField('Salaries and employee benefits',validators=[DataRequired(message=u"Please input integer number"), NumberRange(min=0, max=100000, message="Number is requred")])
    eeffr = FloatField('Efficiency ratio',validators=[DataRequired(message=u"Please input integer number"), NumberRange(min=0, max=1, message="Number should be larger than 0 and least than 1")])
    depdastr = FloatField('Total domestic deposits to total assets',validators=[DataRequired(message=u"Please input integer number"), NumberRange(min=0, max=100000, message="Number is requred")])
    NTRTMMED = FloatField('Amount ($) - time deposits $100,000 to $250,000',validators=[DataRequired(message=u"Please input integer number"), NumberRange(min=0, max=100000, message="Number is requred")])
    elnatry = FloatField('Loan and lease loss provision to assets',validators=[DataRequired(message=u"Please input integer number"), NumberRange(min=0, max=100000, message="Number is requred")])
    nare = FloatField('Loans secured by real estate, total in nonaccrual status',validators=[DataRequired(message=u"Please input integer number"), NumberRange(min=0, max=100000, message="Number is requred")])
    p3re = FloatField('Loans secured by real estate, total past due 30 - 89 days',validators=[DataRequired(message=u"Please input integer number"), NumberRange(min=0, max=100000, message="Number is requred")])
    
    Predict = SubmitField('Predict Bank Valuation')