from wtforms import StringField,  PasswordField, RadioField, ValidationError, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import Length, InputRequired, EqualTo, DataRequired, Email
from models import Researcher
from wtforms import TextField, PasswordField, validators, DateField, IntegerField, SubmitField, FileField, RadioField
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired

login_manager = LoginManager()
# login_manager.setup_app(current_app)


@login_manager.user_loader
def load_user(researcher_id):
    return Researcher.query.get(researcher_id)

class RegistrationForm(Form):
    username = StringField('Username', validators=[InputRequired(), Length(min=3, max=25)])
    email = StringField('Email Address', validators=[Length(min=6, max=35),InputRequired(),Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=80)])
    confirm = PasswordField('Repeat Password', validators=[InputRequired(),
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

class ProjectForm(Form):
    project_name = StringField('Project Name', validators=[Length(min=2, max=25)])
    project_description = StringField('Project Description', validators=[Length(min=15, max=250)])                                                              

class StimuliForm(Form):
   upload = FileField('stimuli', validators=[FileRequired(),FileAllowed(['jpg', 'png','PNG','JPG','jpeg'], 'Images only!')])
   x_resolution = IntegerField('X-Resolution', validators=[Length(min=3, max=4)])
   y_resolution = IntegerField('Y-Resolution', validators=[Length(min=3, max=4)]) 

class DataForm(Form):
   upload = FileField('data', validators=[FileRequired(),FileAllowed(['csv'], 'CSV file only!')])