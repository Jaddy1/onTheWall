from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

import os

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "ontheWall.db"))
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_file
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'S3Kr3t'
  
    db.init_app(app)
    bootstrap = Bootstrap(app)
    application = app

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    #this code was extracted from Digital Ocean: 
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main_blueprint
    app.register_blueprint(main_blueprint)

    from .feed import feed_blueprint
    app.register_blueprint(feed_blueprint)

    @app.template_filter('datetimeformat')
    def datetimeformat(value, format='%B'):
        return value.strftime(format)
    return app