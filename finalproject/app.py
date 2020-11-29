from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
application = app
bootstrap = Bootstrap(app)


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/signup')
def signup():
	return render_template('signup.html')

@app.route('/login')
def login():
	return render_template('login.html')