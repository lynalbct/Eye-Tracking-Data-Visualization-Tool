from flask import Flask, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, url_for,redirect,send_from_directory, request
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
import os
import base64
import csv

upload_folder = 'app/static/user' 
allowed_img_extensions = set(['png', 'jpg', 'jpeg','PNG','JPG'])
allowed_file_extensions = set(['csv'])

def allowed_img(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in allowed_img_extensions

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in allowed_file_extensions

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

@app.route('/<proj_id>/upload/aoi', methods=['GET','POST'])
def upload_stimuli(proj_id):
	form = StimuliForm()
	if request.method == 'POST':
		
		# print 'yes'
		# add project id before the stimuli folder
		# upload_location = upload_folder + '/' + str(current_user.researcher_id) + '/'+'stimuli'
		# print upload_location
		# if os.path.isdir(upload_location) == False:
		# 	os.makedirs(upload_location)
		# print(type(form.upload.data))
		if form.upload is None:
			flash('No selected file')
			return redirect(request.url)

		if form.upload:
			file = form.upload.data
			encoded_string = base64.b64encode(file.read())
			print(type(encoded_string))
			save_stimuli = Stimuli(
					stimuli_name=file.filename,
					upload=encoded_string,
					stimuli_description="stimuli_description",
					x_resolution=form.x_resolution.data,
					y_resolution=form.y_resolution.data,
					project_id=proj_id
				 )
			db.session.add(save_stimuli)
			db.session.commit()
			return redirect(url_for('save_aoi', proj_id=proj_id))
	return render_template('project/define.html', form=form)

@app.route('/stimuli', methods=['GET','POST'])
def stimuli():
	projectform = ProjectForm()
	if request.method == 'POST':
		# check if the data is validated
		if projectform.validate():
			project = Project(
				project_name=projectform.project_name.data,
				project_description = projectform.project_description.data,
				researcher_id = current_user.researcher_id
				)
			# insert data to database
			db.session.add(project)
			db.session.commit()
			projects = Project.query.filter_by(researcher_id=current_user.researcher_id).all()
			return render_template('stimuli/stimuli.html', projects=projects, projectform=projectform)
	else:
		projects = Project.query.filter_by(researcher_id=current_user.researcher_id).all()
		print projects
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



@app.route('/project/<project_id>', methods=['GET','POST'])
def project(project_id):
	if request.method == 'POST':
		if request.files:
			upload_location = upload_folder + '/' + str(current_user.researcher_id) + '/' + str(project_id)
			if os.path.isdir(upload_location) == False:
				os.makedirs(upload_location)
			for i in request.files.getlist('files'):
				filename = secure_filename(i.filename)
				if allowed_file(filename):
					i.save(os.path.join(upload_location + '/', filename))
					save_file = File(
						file_name = filename,
						directory_name = str(upload_location+'/'+filename),
						researcher_id = current_user.researcher_id,
						project_id = project_id
						)
					db.session.add(save_file)
					db.session.commit()
					print 'here'

				else:
					flash('file extension is not csv')
					return redirect(url_for('upload_stimuli',proj_id=project_id))
			return redirect(url_for('upload_stimuli', proj_id=project_id))
		else:
			return redirect(url_for('project',proj_id=project_id))
	return render_template('project/project.html')

@app.route('/<int:proj_id>/analyse', methods=['GET','POST'])
def analyse(proj_id):
	filter_eyemovemnts(proj_id)

	return render_template('project/analyse.html', project_id=proj_id)

def filter_eyemovemnts(proj_id):
	stimuli_data = Stimuli.query.filter_by(project_id=proj_id).first()
	stimuli_id = stimuli_data.stimuli_id
	aoi_data = Aoi.query.filter_by(stimuli_id=stimuli_id).all()
	eye_movement_data = File.query.filter_by(project_id=proj_id).all()
	for i in eye_movement_data:
		upload_location = upload_folder + '/' + str(current_user.researcher_id) + '/' + str(proj_id) + '/' + 'result_'+ i.file_name
		with open(i.directory_name,'r') as csv_file:
			read_csv = csv.reader(csv_file)
			with open(upload_location,'w') as result:
				wtr= csv.writer(result)
				for line in read_csv:
					wtr.writerow((line[0], line[1]))
				with open(upload_location,'r') as new_file:
					file = csv.reader(new_file)
					for a in file:
						print map(int, a[0:])
						
				
				# 	print line[0]

@app.route('/<int:proj_id>/define/aoi', methods=['GET','POST'])
def save_aoi(proj_id):
	data = request.get_json()
	stimuli_data = Stimuli.query.filter_by(project_id=proj_id).first()
	filename = stimuli_data.stimuli_name 
	ext = filename.split('.')[-1]

	if request.method == 'POST':
		for i in range(len(data['startX'])-1):
			print(data['startY'][i])
			print(data['endY'][i])
			print(data['height'][i])
			save_aoi =  Aoi(
				x1 = data['startX'][i],
				y1 = data['startY'][i],
				x2 = data['endX'][i],
				y2 = data['startY'][i],
				x3 = data['startX'][i],
				y3 = (data['endY'][i]),
				x4 = data['endX'][i],
				y4 = (data['endY'][i]),
				stimuli_id = stimuli_data.stimuli_id
				)
			db.session.add(save_aoi)
			db.session.commit()
		return redirect(url_for('analyse', proj_id=proj_id))
	return render_template('project/define_aoi.html', ext=ext, imgdata=stimuli_data.upload, proj_id=proj_id)


@app.route('/project/<projeject_id>')
def temporaryroute(project_id):
	project = Project.query.filter_by(project_id=project_id).first()
	return render_template('project/project.html', project_id=project_id)

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
	return render_template('profile/edit_profile.html', form=form, user=user)

@app.route('/edit_profile')
def editprofile():
	return render_template('profile/edit_profile.html')

@app.route('/logout')
@login_required
def logout():
	session.clear()
	logout_user()
	return redirect(url_for('index'))

