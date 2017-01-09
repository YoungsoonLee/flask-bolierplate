from flask import redirect, render_template, Blueprint, flash
from flask import request, url_for
from flask_login import login_user, logout_user

from user.forms import LoginForm


user_blueprint = Blueprint(
    'users', __name__, template_folder='../templates')
