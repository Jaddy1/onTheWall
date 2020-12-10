from flask import Flask, render_template, request, redirect, Blueprint, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, PasswordField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from datetime import datetime
from . import db
from .models import User
from .models import Post
from .models import Comment
from .models import Category
from flask_login import login_required, current_user

feed_blueprint = Blueprint('feed', __name__)

def category_query():
	return Category.query

class PostForm(FlaskForm):
	postTitle = StringField('Post Title', validators=[DataRequired()])
	postContent = TextAreaField('Post Content', validators=[DataRequired()])
	categoryTitle = QuerySelectField('Category Title', query_factory=category_query,allow_blank=False,get_label='title')
	submit = SubmitField('Submit')

class CommentForm(FlaskForm):
	content = TextAreaField('Comment', validators=[DataRequired()])
	submit = SubmitField('Submit')

class CategoryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class UserAliasForm(FlaskForm):
	alias = StringField('Alias', validators = [DataRequired()])
	password = PasswordField('Password',  validators = [DataRequired()])
	submit = SubmitField('Submit')

#view of all posts
@feed_blueprint.route('/posts')
@login_required
def posts():
	posts = Post.query.order_by(Post.date_created)
	categories = Category.query.order_by(Category.title)
	return render_template('feed.html', posts=posts, categories=categories)

# view of a single post
@feed_blueprint.route('/posts/<int:postId>', methods=['GET'])
@login_required
def viewSinglePost(postId=None):
	form = CommentForm()
	postNum = request.args.get('posts', postId)
	post = Post.query.filter_by(postId=postNum).first()
	comments = Comment.query.filter_by(postId=postNum).order_by(Comment.date_created)
	return render_template('singlePost.html', post=post, form=form, comments=comments)

# create a post
@feed_blueprint.route('/createPost', methods=['POST', 'GET'])
@login_required
def createPost():
	form = PostForm()
	form.categoryTitle.query = Category.query.order_by(Category.title)
	if request.method == "POST":
		post_title = request.form['postTitle']
		post_content = request.form['postContent']
		category_title = form.categoryTitle.data.title
		category = Category.query.filter_by(title=category_title).first()	
		new_post = Post(title=post_title, content=post_content, userId=current_user.id, categoryId=category.id)
		try:
			db.session.add(new_post)
			db.session.commit()
			return redirect('/posts')
		except:
			flash ("Something went wrong...", "alert-error")
			return redirect('/createPost')
	else:
		return render_template('createPost.html', form=form)

#comment a post	
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
			flash ("Something went wrong...", "alert-error")
			return redirect('/posts')
	else:
		return render_template('singlePost.html', form=form, post=post)

#like a post
@feed_blueprint.route('/posts/<int:postId>/<action>')
@login_required
def likePost(postId, action):
	postNum = request.args.get('posts', postId)	
	post = Post.query.filter_by(postId=postNum).first()
	if action == 'like':
			User.like(current_user,post)
			db.session.commit()
			return redirect(request.referrer)
	if action == 'unlike':
		current_user.unlike(post)
		db.session.commit()
		return redirect(request.referrer)
	return redirect('/')

#create new category
@feed_blueprint.route('/createCategory', methods = ['POST', 'GET'])
@login_required
def createCategory():
	form = CategoryForm()
	if request.method == "POST":
		title = request.form['title']
		description = request.form['description']
		new_category = Category(title=title, description=description, userId= current_user.id, alias=" ")
		try:
			db.session.add(new_category)
			db.session.commit()
			return redirect('/posts')
		except:
			flash ("Something went wrong...", "alert-error")
			return redirect('/createCategory')
	else:
		return render_template('createCategory.html', form=form)


#view all posts in one category
@feed_blueprint.route('/categories/<int:categoryId>', methods=['GET'])
@login_required
def viewPostsInCategory(categoryId=None):
	categoryId = request.args.get('categories', categoryId)
	category = Category.query.filter_by(id = categoryId).first()
	posts = Post.query.join(Category).filter_by(id = categoryId).order_by(Post.date_created)
	return render_template('postsInCategory.html', posts = posts, category = category)

#create an alias

@feed_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def alias():
	form = UserAliasForm()
	if request.method == "POST":
		userId = current_user.id 
		alias = request.form['alias']
		password = request.form['password']
		user = User.query.filter_by(id=userId).first()
		if user.verify_password(password): 
			user.alias = alias
			db.session.commit()
			flash("Looks like you have a new alias!", "alert-info")
			return redirect(request.referrer)
		else:
			flash("Something went wrong...", "alert-error")
	return render_template('profile.html', form=form)


