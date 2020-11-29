from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from datetime import datetime

app = Flask(__name__)
application = app
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///post.db'

db = SQLAlchemy(app)

class PostForm(FlaskForm):
    postTitle = StringField('Post Title', validators=[DataRequired()])
    postContent = TextAreaField('Post Content', validators=[DataRequired()])
    submit = SubmitField('Submit')

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(200), nullable=False)
	content = db.Column(db.String(1000), nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return '<Post %t>' % self.title


@app.route('/')
def index():
	posts = Post.query.order_by(Post.date_created)
	return render_template('index.html', posts=posts)

@app.route('/signup')
def signup():
	return render_template('signup.html')

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/createPost', methods=['POST', 'GET'])
def createPost():
	form = PostForm()
	if request.method == "POST":
		post_title = request.form['postTitle']
		post_content = request.form['postContent']
		new_post = Post(title=post_title, content=post_content)

		try:
			db.session.add(new_post)
			db.session.commit()
			return redirect('/')
		except:
			return redirect('/createPost')
	else:
		return render_template('createPost.html', form=form)