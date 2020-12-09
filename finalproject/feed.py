from flask import Flask, render_template, request, redirect, Blueprint
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from datetime import datetime
from . import db
from .models import User
from .models import Post
from .models import Comment
from flask_login import login_required, current_user
from sqlalchemy import desc

feed_blueprint = Blueprint('feed', __name__)

class PostForm(FlaskForm):
    postTitle = StringField('Post Title', validators=[DataRequired()])
    postContent = TextAreaField('Post Content', validators=[DataRequired()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
	content = StringField('Comment', validators=[DataRequired()])
	submit = SubmitField('Submit')

def sortPosts(filter):
	if(filter == "old"):
		return Post.query.order_by(Post.date_created.desc())
	else:
		return Post.query.order_by(Post.date_created)

@feed_blueprint.route('/posts', methods=['GET', 'POST'])
@login_required
def posts():
	posts = Post.query.order_by(Post.date_created.desc())
	if request.method == "POST":
		posts = sortPosts(request.form['sort'])
		return render_template('feed.html', posts=posts, userId=current_user.id)
	else:
		return render_template('feed.html', posts=posts, userId=current_user.id)

@feed_blueprint.route('/posts/<int:postId>', methods=['GET'])
@login_required
def viewSinglePost(postId=None):
	form = CommentForm()
	postNum = request.args.get('posts', postId)
	post = Post.query.filter_by(postId=postNum).first()
	comments = Comment.query.filter_by(postId=postNum).order_by(Comment.date_created)
	return render_template('singlePost.html', post=post, form=form, comments=comments)

@feed_blueprint.route('/createPost', methods=['POST', 'GET'])
@login_required
def createPost():
	form = PostForm()
	if request.method == "POST":
		post_title = request.form['postTitle']
		post_content = request.form['postContent']
		new_post = Post(title=post_title, content=post_content, userId=current_user.id)
		try:
			db.session.add(new_post)
			db.session.commit()
			return redirect('/posts')
		except:
			return redirect('/createPost')
	else:
		return render_template('createPost.html', form=form)

@feed_blueprint.route('/updatePost/<int:postId>', methods=['GET', 'POST'])
@login_required
def updatePost(postId):
	post = Post.query.get_or_404(postId)
	update_post = Post.query.get_or_404(postId)

	if request.method == "POST":
		update_post.title = request.form['postTitle']
		update_post.content = request.form['postContent']

		try:
			db.session.commit()
			return redirect('/posts')
		except:
			return "Problem updating post"
	else:
		form = PostForm()
		return render_template('updatePost.html', post=post, form=form)

@feed_blueprint.route('/deletePost/<int:postId>', methods=['GET'])
@login_required
def deletePost(postId):
	delete_post = Post.query.get_or_404(postId)

	try:
		db.session.delete(delete_post)
		db.session.commit()
		return redirect('/posts')
	except:
		return "Problem deleting that post"

@feed_blueprint.route('/posts/<int:postId>', methods=['POST'])
@login_required
def commentPost(postId=None):	
	postNum = request.args.get('posts', postId)	
	post = Post.query.filter_by(postId=postNum).first()
	form = CommentForm()
	if form.validate_on_submit():
		content = request.form['content']
		new_comment = Comment(content=content,userId=current_user.id,postId=postNum)
		try:
			db.session.add(new_comment)
			db.session.commit()
			return redirect(request.referrer)
		except:
			return redirect('/posts')
	else:
		return render_template('singlePost.html', form=form, post=post)

@feed_blueprint.route('/posts/<int:postId>/<action>')
@login_required
def likePost(postId, action):
	postNum = request.args.get('posts', postId)	
	post = Post.query.filter_by(postId=postNum).first()
	print(action)
	if action == 'like':
			User.like(current_user,post)
			db.session.commit()
			return redirect(request.referrer)
	if action == 'unlike':
		current_user.unlike(post)
		db.session.commit()
		return redirect(request.referrer)
	return redirect('/')