from flask import Flask, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, url_for,redirect,send_from_directory
from app import db, app
from app.forms import *
from app.models import *
from flask import render_template, request, url_for,redirect,send_from_directory
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask import flash
from flask import current_app
from werkzeug.security import check_password_hash
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

upload_folder = 'app/static/user'
allowed_extensions = set(['csv', 'png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def debug():
	assert current_app.debug == False, "Don't panic! You're here by request of debug()"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(researcher_id):
	return Researcher.query.get(researcher_id)

@app.route('/')
def index():
	return render_template('landing/landing.html')

@app.route('/forgotpassword')
def forgotpassword():
	return render_template('dashboard/forgot-password.html')

@app.route('/prof')
def prof():
	user = Researcher.query.filter_by(researcher_id=current_user.researcher_id)
	return render_template('profile/profile.html', user=user)

@app.route('/stimuli', methods=['GET','POST'])
def stimuli():
	projectform = ProjectForm()
	if request.method == 'POST':
		if projectform.validate():
			project = Project(
				project_name=projectform.project_name.data,
				project_description = projectform.project_description.data,
				researcher_id = current_user.researcher_id
				)
			db.session.add(project)
			db.session.commit()
	else:
		projects = Project.query.filter_by(researcher_id=current_user.researcher_id).all()
		for a in projects:
			project_count = 0
			project_count = len(projects)+1
		print(project_count)
		return render_template('stimuli/stimuli.html', projectform=projectform, projects=projects)
	return render_template('stimuli/stimuli.html', projectform=projectform)


@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if current_user.is_authenticated is True:
		return redirect(url_for('home'))
	elif form.validate_on_submit():
		user = Researcher.query.filter_by(username=form.username.data).first()
		if user:
			print(form.password.data)
			if check_password_hash(user.password, form.password.data):
				login_user(user, remember=True)
				session["current_user"] = {
					"first_name": "",
					"last_name": "",
					"researcher_id": current_user.researcher_id,
					"profession": "",
					"organization": ""
				}
				return redirect(url_for('home'))
			else:
				flash('Invalid username or password')
				return render_template('forms/login.html', form=form)
		else:
			return render_template('forms/login.html', form=form)
	return render_template('forms/login.html', form=form)

@app.route('/register', methods = ['GET','POST'])
def register():
	form = RegistrationForm()
	if request.method == 'POST':
		if form.validate():
			new_user = Researcher(
				username=form.username.data,
				email=form.email.data,
				password=form.password.data,
				)
			print(new_user)
			db.session.add(new_user)
			db.session.commit()
			login_user(new_user, remember=True)
			session["current_user"] = {
				"first_name": "",
				"last_name": "",
				"researcher_id": current_user.researcher_id,
				"profession": "",
				"organization": ""
			}
			account = Researcher.query.filter_by(researcher_id=current_user.researcher_id).first()
			if account:
				add_researcher = Connection(researcher_id=account.researcher_id)
				db.session.add(add_researcher)
				db.session.commit()
			return redirect(url_for('info'))
		else:
			print(form.errors)
	return render_template('forms/registration.html', form=form)

@app.route('/info', methods = ['GET','POST'])
@login_required
def info():
	form = InfoForm()
	if request.method == 'POST':
		if form.validate():
			current_user.first_name = form.first_name.data,
			current_user.last_name = form.last_name.data,
			current_user.profession = form.profession.data,
			current_user.organization = form.organization.data
			db.session.add(current_user)
			db.session.commit()
			print('ok')
			return redirect(url_for('home'))
		else:
			return redirect(url_for('info'))
	return render_template('forms/info.html', form=form)

@app.route('/createproject', methods=['GET','POST'])
def createproject():
	projectform = ProjectForm()
	if request.method == 'POST':
		if form.validate():
			project = Project(
				project_name=projectform.project_name,
				project_description = projectform.project_description
				)
			db.session.add(project)
			db.session.commit()

	return render_template('stimuli/stimuli.html', projectForm=form)

@app.route('/project/<int:project_id>', methods=['GET','POST'])
def project(project_id):


	return render_template('project/project.html')

@app.route('/resetpassword')
def resetpassword():
	form = ResetPasswordForm()
	if request.method == 'POST':
		if form.validate():
			current_user.username=form.username.data,
			current_user.email=form.email.data,
			current_user.password = form.password.data
			current_user.first_name = form.first_name.data,
			current_user.last_name = form.last_name.data,
			current_user.profession = form.profession.data,
			current_user.organization = form.organization.data
			db.session.add(current_user)
			db.session.commit()
			print('ok')
		else:
			print('not validated')
	return render_template('profile/profile.html')

@app.route('/home')
def home():
	user = Researcher.query.filter_by(researcher_id=current_user.researcher_id).first()
	return render_template('dashboard/index.html', user=user)

@app.route('/connections',methods=['GET','POST'])
def connections():
	connections = Connection.query.filter_by(researcher_id=current_user.researcher_id).all()
	not_connections = Connection.query.filter(Connection.researcher_id != current_user.researcher_id).all()
	not_connected_ids,not_connected_fname, not_connected_lname = [], [], []
	for not_connection in not_connections:
		not_connected_user = Researcher.query.filter_by(researcher_id=not_connection.researcher_id).all()



	return render_template('connections/connections.html', not_connected_user=not_connected_user)


@app.route('/profile', methods=['POST','GET'])
def profile():
	form = ProfileForm()
	print(form)
	user = Researcher.query.filter_by(researcher_id =current_user.researcher_id).first()
	print(current_user.researcher_id)
	if request.method == 'POST':
		if form.validate():
			current_user.username=form.username.data,
			current_user.email=form.email.data,
			current_user.first_name = form.first_name.data,
			current_user.last_name = form.last_name.data,
			current_user.profession = form.profession.data,
			current_user.organization = form.organization.data
			db.session.add(current_user)
			db.session.commit()
			print('ok')
		else:
			print('not validated')
	return render_template('profile/profile.html', form=form, user=user)

@app.route('/logout')
@login_required
def logout():
	session.clear()
	logout_user()
	return redirect(url_for('index'))

