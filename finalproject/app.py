from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
application = app
bootstrap = Bootstrap(app)


db= SQLAlchemy(app)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(200), nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/signup')
def signup():
	return render_template('signup.html')

@app.route('/login')
def login():
	return render_template('login.html')