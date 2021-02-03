from car_api import app, db
from flask import render_template, request, redirect, url_for

from car_api.forms import UserLoginForm
from car_api.models import User

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods = ['GET','POST'])
def signup():
    form = UserLoginForm()


    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print(email, password)

        user = User(email, password = password)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('signin'))


    return render_template('signup.html', form=form)

@app.route('/signin', methods = ['GET','POST'])
def signin():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email,password)
    except:
        raise Exception('Invalid Form Data: Please Check your form')
    return render_template('signin.html', form = form)