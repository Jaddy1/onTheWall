from flask import Blueprint, render_template, redirect, url_for,request, flash
from . import db
from .models import User
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods =['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        email = request.form.get('inputEmail')
        password = request.form.get('inputPassword')
        remember = True if request.form.get('remember') else False
        user = User.query.filter_by(email=email).first()
        if not user or not user.verify_password(password):
            print("Please check your login details and try again.")
            return redirect(url_for('auth.login'))
        login_user(user, remember=remember)
        return redirect(url_for('main.feed'))

@auth_blueprint.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        email = request.form.get('inputEmail')
        password = request.form.get('inputPassword')
        user = User.query.filter_by(email=email).first() 
        if user:
            return redirect(url_for('auth.signup'))
        new_user = User(email=email, password_hash=generate_password_hash(password, method='sha1'))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))

@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.main'))
