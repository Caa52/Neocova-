from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, PredictForm
from app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
import pickle
import numpy as np

posts = [
    {
        'author': 'Alice',
        'title': 'WUSTL',
        'content': 'HELLO',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Vicky',
        'title': 'WUSTL',
        'content': 'Good morning',
        'date_posted': 'April 21, 2018'
    }
]

var = ["eqtot","eq","IDP3REDM","IDNAREDM"]

model = pickle.load(open('model.pkl', 'rb'))


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')

@app.route("/base")
@login_required
def base():
    return render_template('base.html', title='Account')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    form = PredictForm()
    return render_template('predict_form.html',title='Login', form=form)


@app.route('/result',methods=['POST'])
def result():

    int_features = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = round(prediction[0], 2)

    return render_template('predict.html', prediction_text='Your bank evaluation is estimated as $ {}'.format(output))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@app.route('/404')
def e404e():
    return render_template('404.html')
