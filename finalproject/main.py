from flask import Flask, Blueprint,render_template, redirect, request, flash
from . import db 
from flask_login import UserMixin, LoginManager, login_user, login_required
import os 

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def main():
	return 'Main'

#login_manager = LoginManager()
#login_manager.login_view = 'auth.login'

#@login_manager.user_loader
#def load_user(user_email):
    #return User.query.get(String(email))

#def create_app(config_name):
   #from .auth import auth as auth_blueprint
   #app.register_blueprint(auth_blueprint, url_prefix='/auth')
    #login_manager.init_app(app)
   # return app

#Setting user table
#class User(UserMixin, db.Model):
	#email = db.Column(db.String(100), primary_key = True)
	#password_hash = db.Column(db.String(100))

#def password(self, password):
   # self.password_hash = generate_password_hash(password)
#def verify_password(self, password):
    #return check_password_hash(self.password_hash, password)

#Setting post table
#class Post(db.Model):
#	postId = db.Column(db.Integer, primary_key = True)
#	title = db.Column(db.String(100))
#	content = db.Column(db.String(100)) 
#	email = db.Column(db.String(100), db.ForeignKey('user.email'))

#class SignInForm(FlaskForm): 
#	email = StringField('Email', validators=[DataRequired(),Email()])
#	password = PasswordField('Password', validators=[DataRequired()])
#	submit = SubmitField('Sign In')

#class SignUpForm(FlaskForm):
#	email = StringField('Email', validators=[DataRequired(),Email()])
#	password = PasswordField('Password', validators=[DataRequired()])
#	submit = SubmitField('Sign Up')


#@app.route('/login', methods=['GET', 'POST'])
#def signin():
	#if request.method=='GET':
       # emailData = request.args.form['inputEmail']
       # passwordData = request.form['inputPassword']
       # user = User.query.filter_by(email=emailData).first()
       # if user is not None and user.verify_password(passwordData):
	       # login_user(user)
	       # next = request.args.get('next')
	       # if next is None or not next.startswith('/'):
	           # next = url_for('main.index')
	           # return redirect(next)
	           # flash('Invalid username or password.')
   # return render_template('login.html', form=form)
