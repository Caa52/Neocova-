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
        user = User(username=form.username.data, email=form.email.data, City = form.City.data, State = form.State.data, Zip = form.Zip.data, Company = form.Company.data, Department = form.Department.data, Title = form.Title.data, password=hashed_password)
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
        Var_features = ['roeinjr','noijy','asset','RBCT1J','core_deposit','lnlsntv','County_GDP_Percent','PC_Labor_Force','PC_Unemployed','GR_Total_Population']
        s_Var_features = ['s_roeinjr','s_noijy','s_asset','s_RBCT1J','s_core_deposit','s_lnlsntv','s_County_GDP_Percent','s_PC_Labor_Force','s_PC_Unemployed','s_GR_Total_Population']
        
        s_final_features = [None] * len(s_Var_features)
        final_features = np.zeros(len(Var_features))

        s_final_features[0] = form.s_roeinjr.data
        s_final_features[1] = form.s_noijy.data
        s_final_features[2] = form.s_asset.data
        s_final_features[3] = form.s_RBCT1J.data
        s_final_features[4] = form.s_core_deposit.data
        s_final_features[5] = form.s_lnlsntv.data
        s_final_features[6] = form.s_County_GDP_Percent.data
        s_final_features[7] = form.s_PC_Labor_Force.data
        s_final_features[8] = form.s_PC_Unemployed.data
        s_final_features[9] = form.s_GR_Total_Population.data

        final_features[0] = form.roeinjr.data
        final_features[1] = form.noijy.data
        final_features[2] = form.asset.data
        final_features[3] = form.RBCT1J.data
        final_features[4] = form.core_deposit.data
        final_features[5] = form.lnlsntv.data
        final_features[6] = form.County_GDP_Percent.data
        final_features[7] = form.PC_Labor_Force.data
        final_features[8] = form.PC_Unemployed.data
        final_features[9] = form.GR_Total_Population.data

        for i in range(0,len(s_final_features)):
            if s_final_features[i] == '2':
                final_features[i] = final_features[i]*(-1)

        final_features = [final_features.tolist()]
        
        scoring_uri = 'http://5e56fe7c-6b6f-47ff-bdfb-fac9b4b8c334.westus2.azurecontainer.io/score'
     
        data = {"data": final_features}
        input_data = json.dumps(data)
        headers= {'Content-Type': 'application/json'}
        resp = requests.post(scoring_uri, input_data, headers=headers)
        
        output  = json.loads(resp.text)
        # output  = resp.text
        output = round(output[0][0]*100,3);

        history = History(roeinjr = final_features[0][0],
            noijy = final_features[0][1],
            asset = final_features[0][2],
            RBCT1J= final_features[0][3],
            core_deposit= final_features[0][4],
            lnlsntv= final_features[0][5],
            County_GDP_Percent= final_features[0][6],
            PC_Labor_Force= final_features[0][7],
            PC_Unemployed = final_features[0][8],
            GR_Total_Population = final_features[0][9],

            output = output,
            time = datetime.now())

        found_user = User.query.filter_by(username=current_user.username).first()
        found_user.history.append(history)
        # db.create_all()
        db.session.add(found_user)
        db.session.add(history)
        db.session.commit()
        return render_template('predict_form.html', title='Login', form=form, prediction_text='Your bank evaluation is estimated to have {} % change'.format(output))

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

