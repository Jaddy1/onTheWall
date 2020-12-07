from . import db
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique = True)
    password_hash = db.Column(db.String(100))
    posts = db.relationship('Post', backref='user')
    comments = db.relationship('Comment', backref='user')
    likes = db.relationship('Likes', backref='user')

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def like(self, post):
        if not self.check_like(post):
            new_like = Likes(userId=self.id,postId=post.postId)
            db.session.add(new_like)

    def unlike(self, post):
        if self.check_like(post):
            Likes.query.filter_by(userId=self.id, postId=post.postId).delete()

    def check_like(self, post):
        return Likes.query.filter_by(userId=self.id, postId=post.postId).count() > 0

class Post(db.Model):
    postId = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(100)) 
    userId = db.Column(db.String(100), db.ForeignKey('user.id'))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='post')
    likes = db.relationship('Likes', backref='post')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    content = db.Column(db.String(160))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    postId = db.Column(db.Integer, db.ForeignKey('post.postId'))

class Likes(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    postId = db.Column(db.Integer, db.ForeignKey('post.postId'))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    
