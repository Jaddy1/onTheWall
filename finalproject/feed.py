from flask import Flask, render_template, request, redirect, Blueprint
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from datetime import datetime
from . import db
from .models import Post
from flask_login import login_required

feed_blueprint = Blueprint('feed', __name__)

class PostForm(FlaskForm):
    postTitle = StringField('Post Title', validators=[DataRequired()])
    postContent = TextAreaField('Post Content', validators=[DataRequired()])
    submit = SubmitField('Submit')

# class Post(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
# 	title = db.Column(db.String(200), nullable=False)
# 	content = db.Column(db.String(1000), nullable=False)
# 	date_created = db.Column(db.DateTime, default=datetime.utcnow)

# 	def __repr__(self):
# 		return '<Post %t>' % self.title


@feed_blueprint.route('/posts')
@login_required
def posts():
	posts = Post.query.order_by(Post.date_created)
	return render_template('feed.html', posts=posts)

# #@app.route('/signup')
# def signup():
# 	return render_template('signup.html')

# @app.route('/login')
# def login():
# 	return render_template('login.html')

@feed_blueprint.route('/createPost', methods=['POST', 'GET'])
@login_required
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