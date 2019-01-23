from flask import current_app, request, render_template, redirect, url_for
# from myapp.models import User
from flask.ext.login import LoginManager, login_user, logout_user, login_required, current_user
from wtforms import Form, TextField, PasswordField, validators


login_manager = LoginManager()
login_manager.setup_app(current_app)


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


class LoginForm(Form):
    username = TextField('Username', [validators.Required(), validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.Required(), validators.Length(min=6, max=200)])

