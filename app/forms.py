from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

from wtforms import StringField,  PasswordField, RadioField, ValidationError, SelectField, SubmitField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import Length, InputRequired, EqualTo, DataRequired, Email, ValidationError
from app.models import Researcher
from wtforms import TextField, PasswordField, validators, DateField, IntegerField, SubmitField, FileField, RadioField
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import Form, FlaskForm

login_manager = LoginManager()
# login_manager.setup_app(current_app)


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)

class RegistrationForm(Form):
    username = StringField('Username', validators=[InputRequired(), Length(min=3, max=25)])
    email = StringField('Email Address', validators=[Length(min=6, max=35),InputRequired(),Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=80)])
    confirm = PasswordField('Repeat password', validators=[InputRequired(),
                                                           EqualTo('password', message='Passwords must match.')])

    def validate_email(self, field):
        if Researcher.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if Researcher.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')



class LoginForm(Form):
    username = StringField('Username', validators=[InputRequired(), Length(min=3, max=25)])
    password = PasswordField('Password', validators=[InputRequired(),Length(min=6, max=80)])

class ProfileForm(Form):
    first_name = StringField('First Name', validators=[Length(min=2, max=25)])
    last_name = StringField('Last Name', validators=[Length(min=2, max=25)])
    username = StringField('Username', validators=[InputRequired(), Length(min=3, max=25)])
    profession = StringField('Profession', validators=[Length(min=4, max=25)])
    organization = StringField('Organization', validators=[Length(min=4, max=25)])
    email = StringField('Email Address', validators=[Length(min=6, max=35),InputRequired(),Email()])

    def validate_email(self, field):
        if Researcher.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if Researcher.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

class InfoForm(Form):
    first_name = StringField('First Name', validators=[Length(min=2, max=25)])
    last_name = StringField('Last Name', validators=[Length(min=2, max=25)])
    profession = StringField('Profession', validators=[Length(min=4, max=25)])
    organization = StringField('Organization', validators=[Length(min=4, max=25)])

class ResetPasswordForm(Form):
    first_name = StringField('First Name', validators=[Length(min=2, max=25)])
    last_name = StringField('Last Name', validators=[Length(min=2, max=25)])
    username = StringField('Username', validators=[InputRequired(), Length(min=3, max=25)])
    profession = StringField('Profession', validators=[Length(min=4, max=25)])
    organization = StringField('Organization', validators=[Length(min=4, max=25)])
    email = StringField('Email Address', validators=[Length(min=6, max=35),InputRequired(),Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=80)])

    def validate_email(self, field):
        if Researcher.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if Researcher.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')



class UpdateAccountForm(FlaskForm):

    first_name = StringField('First Name',validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name',validators=[DataRequired(), Length(min=2, max=20)])
    profession = StringField('Profession',validators=[Length(min=2, max=20)])
    organization = StringField('Organization',validators=[Length(min=2, max=20)])
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

