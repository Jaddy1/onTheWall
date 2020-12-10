from flask import Flask, Blueprint,render_template, redirect, request, flash
from . import db 
from flask_login import login_required, current_user
import os 

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def main():
	return render_template('main.html')

# @main_blueprint.route('/feed')
# @login_required
# def feed():
# 	return render_template('feed.html')
