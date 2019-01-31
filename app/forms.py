from wtforms import StringField,  PasswordField, RadioField, ValidationError, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import Length, InputRequired, EqualTo, DataRequired
from models import Researcher
from wtforms import TextField, PasswordField, validators
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import Form

# login_manager = LoginManager()
# # login_manager.setup_app(current_app)


# @login_manager.user_loader
# def load_user(userid):
#     return User.query.get(userid)

class RegistrationForm(Form):
    username = StringField('Username', validators=[InputRequired(), Length(min=3, max=25)])
    first_name = StringField('First Name', [validators.Length(min=2, max=25)])
    middle_name = StringField('Middle Name', [validators.Length(min=4, max=25)])
    last_name = StringField('Last Name', [validators.Length(min=4, max=25)])
    profession = StringField('Profession', [validators.Length(min=4, max=25)])
    organization = StringField('Organization', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=80)])
    confirm = PasswordField('Repeat password', validators=[DataRequired(),
                                                           EqualTo('password', message='Passwords must match.')])

    def validate_email(self, field):
        if Researcher.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if Researcher.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')




class LoginForm(Form):
    username = TextField('Username', [validators.Required(), validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.Required(), validators.Length(min=6, max=200)])

