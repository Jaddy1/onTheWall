from flask import Flask, render_template, redirect, request, flash
from flask import Blueprint
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_login import login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_login import login_required

import os 

auth = Blueprint('auth', __name__)

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "ontheWall.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
application = app

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_email):
    return User.query.get(String(email))

def create_app(config_name):
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    login_manager.init_app(app)
    return app

#Setting user table
class User(UserMixin, db.Model):
	email = db.Column(db.String(100), primary_key = True)
	password_hash = db.Column(db.String(100))

def password(self, password):
    self.password_hash = generate_password_hash(password)
def verify_password(self, password):
    return check_password_hash(self.password_hash, password)

#Setting post table
class Post(db.Model):
	postId = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(100))
	content = db.Column(db.String(100)) 
	email = db.Column(db.String(100), db.ForeignKey('user.email'))

class SignInForm(FlaskForm): 
	email = StringField('Email', validators=[DataRequired(),Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Sign In')

class SignUpForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(),Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Sign Up')


@app.route('/login', methods=['GET', 'POST'])
def signin():
    form = SignInForm()
    emailData = request.form.get("email")
    passwordData = request.form.get("password")
    user = User.query.filter_by(email=emailData).first()
    if user is not None and user.verify_password(passwordData):
	    login_user(user)
	    next = request.args.get('next')
	    if next is None or not next.startswith('/'):
	        next = url_for('main.index')
	    return redirect(next)
	    flash('Invalid username or password.')
    return render_template('login.html', form=form)


@app.route('/', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
	    email = request.form.get("email")
	    password = request.form.get("password")
	    user = User(email, password)
	    db.session.add(user)
	    db.session.commit()
	    flash('You can now login.')
	    return redirect(url_for('login'))
    return render_template('signup.html', form=form)