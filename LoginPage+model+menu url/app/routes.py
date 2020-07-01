from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm
from app.models import User, Post, History
from flask_login import login_user, current_user, logout_user, login_required
import pickle
import numpy as np
from datetime import datetime
import json
import requests 

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


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    return render_template('predict.html')


@app.route('/result',methods=['POST'])
def result():

    final_features = [int(x) for x in request.form.values()]
    
    scoring_uri = 'http://43aa851b-4045-482b-9016-9f97cc6b3e70.westus2.azurecontainer.io/score'
 
    data = {"data": final_features}
    input_data = json.dumps(data)
    headers= {'Content-Type': 'application/json'}
    resp = requests.post(scoring_uri, input_data, headers=headers)
    output  = json.loads(resp.text)
    output = round(output['predict'][0], 2)

    history = History(input1 = final_features[0],
        input2 = final_features[1],
        input3 = final_features[2],
        output = output,
        time = datetime.now())

    found_user = User.query.filter_by(username=current_user.username).first()
    found_user.history.append(history)
    # db.create_all()
    db.session.add(found_user)
    db.session.add(history)
    db.session.commit()

    return render_template('predict.html', prediction_text='Your bank valuation is estimated as $ {}'.format(output))

@app.route("/view")
def view():
    return render_template("view.html", values=History.query.all())

@app.route("/viewaccount")
def viewaccount():
    return render_template("viewaccount.html", values=User.query.all())


