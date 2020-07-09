from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, PredictForm
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

# model = pickle.load(open('model.pkl', 'rb'))


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


# @app.route('/predict', methods=['GET', 'POST'])
# def predict():
#     return render_template('predict.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    form = PredictForm()
    if form.validate_on_submit():
        final_features = np.zeros(18)
        final_features[0] = form.eqtot.data
        final_features[1] = form.eq.data
        final_features[2] = form.IDP3REDM.data
        final_features[3] = form.IDNAREDM.data
        final_features[4] = form.RBCT1J.data
        final_features[5] = form.liabeq.data
        final_features[6] = form.Lnrenr2N.data
        final_features[7] = form.crcon.data
        final_features[8] = form.crci.data
        final_features[9] = form.Lnag1.data
        final_features[10] = form.intexpy.data
        final_features[11] = form.esal.data
        final_features[12] = form.eeffr.data
        final_features[13] = form.depdastr.data
        final_features[14] = form.NTRTMMED.data
        final_features[15] = form.elnatry.data
        final_features[16] = form.nare.data
        final_features[17] = form.p3re.data
        final_features = [final_features.tolist()]
        
        scoring_uri = 'http://b4f7f8bc-8a7f-42fc-8759-b17db8bb8b22.westus2.azurecontainer.io/score'
     
        data = {"data": final_features}
        input_data = json.dumps(data)
        headers= {'Content-Type': 'application/json'}
        resp = requests.post(scoring_uri, input_data, headers=headers)
        
        output  = json.loads(resp.text)
        # output  = resp.text
        output = output[0][0]

        history = History(input1 = final_features[0][0],
            input2 = final_features[0][1],
            input3 = final_features[0][2],
            output = output,
            time = datetime.now())

        found_user = User.query.filter_by(username=current_user.username).first()
        found_user.history.append(history)
        # db.create_all()
        db.session.add(found_user)
        db.session.add(history)
        db.session.commit()
        return render_template('predict_form.html', title='Login', form=form, prediction_text='Your bank evaluation is estimated as $ {}'.format(output))

    return render_template('predict_form.html',title='Login', form=form)

@app.route("/view")
def view():
    return render_template("view.html", values=History.query.all())

@app.route("/viewaccount")
def viewaccount():
    return render_template("viewaccount.html", values=User.query.all())

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

# @app.errorhandler(500)
# def internal_error(error):
#     return render_template('500.html'), 500

@app.route('/404')
def e404e():
    return render_template('404.html')

