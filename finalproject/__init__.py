from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_bootstrap import Bootstrap
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

    #this code was extracted from Digital Ocean: 
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main_blueprint
    app.register_blueprint(main_blueprint)

    return app