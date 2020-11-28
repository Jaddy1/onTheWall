from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    email = db.Column(db.String(100), primary_key = True)
    password_hash = db.Column(db.String(100))

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
	postId = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(100))
	content = db.Column(db.String(100)) 
	email = db.Column(db.String(100), db.ForeignKey('user.email'))