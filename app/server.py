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
from array import *
import re
import operator
import numpy as np
import itertools
import glob
import ast
from itertools import permutations
from itertools import combinations
# import pandas as pd


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
			# if account:
			# 	add_researcher = Connection(researcher_id=account.researcher_id)
			# 	db.session.add(add_researcher)
			# 	db.session.commit()
			print 'ok'
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

@app.route('/<int:proj_id>/upload/aoi', methods=['GET','POST'])
def upload_stimuli(proj_id):
	form = StimuliForm()
	if request.method == 'POST':
		
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
		print projectform.project_name.data
		print projectform.project_description.data
		if projectform.validate():
			project = Project(
				project_name=projectform.project_name.data,
				project_description = projectform.project_description.data,
				researcher_id = current_user.researcher_id
				)
			db.session.add(project)
			db.session.commit()
			return redirect(url_for('project',project_id=project.project_id))
		else:
			print(projectform.errors)
	else:
		print 'here'
		projects = Project.query.filter_by(researcher_id=current_user.researcher_id).all()
		print projects
		return render_template('stimuli/stimuli.html', projects=projects, projectform=projectform)
	return render_template('stimuli/stimuli.html', projectform=projectform)


@app.route('/project/<int:project_id>', methods=['GET','POST'])
def project(project_id):
	if request.method == 'POST':
		if request.files:
			upload_location = upload_folder + '/' + str(current_user.researcher_id) + '/' + str(project_id)
			orig_location = upload_folder + '/' + str(current_user.researcher_id) + '/' + str(project_id)+'/original'

			if os.path.isdir(upload_location) == False:
				os.makedirs(upload_location)
				os.makedirs(orig_location)
			for i in request.files.getlist('files'):
				filename = secure_filename(i.filename)
				if allowed_file(filename):
					i.save(os.path.join(upload_location + '/', filename))
					i.save(os.path.join(orig_location +'/', filename))
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

@app.route('/view/<int:project_id>', methods=['GET','POST'])
def view_project(project_id):
	project = Project.query.filter_by(project_id=project_id).first()
	file = File.query.filter_by(project_id=project_id).all()
	stimuli = Stimuli.query.filter_by(project_id=project_id).first()
	filename = stimuli.stimuli_name 
	ext = filename.split('.')[-1]
	array_size = []
	for data in file:
		size = os.path.getsize(data.directory_name)
		array_size.append(size)

	return render_template('project/view_project.html',array=zip(file,array_size),\
		project=project,files=file,stimuli=stimuli,ext=ext,imgdata=stimuli.upload)


@app.route('/<int:proj_id>/analyse', methods=['GET','POST'])
def analyse(proj_id):
	sequences = []
	base_loc = upload_folder + '/' + str(current_user.researcher_id) + '/' + str(proj_id)
	with open(base_loc+'/processed.csv','r') as read_file:
		reader = csv.reader(read_file)
		for rows in reader:
			data = re.sub(r'[^A-Za-z]', '', str(rows)) 
			sequences.append(data)
		# postprocess(proj_id)
	return render_template('project/analyse.html',sequences=sequences, proj_id=proj_id)


def caller(proj_id):
	eye_movement_data = File.query.filter_by(project_id=proj_id).all()
	counter = len(eye_movement_data)
	num = 0
	for i in eye_movement_data:
		print num
		if num < counter:
			num = num + 1
		filter_aoi(i.directory_name,i.file_name,proj_id)
		clean_data(i.directory_name,i.file_name,proj_id)
		final_preprocess(i.directory_name,i.file_name,proj_id)
		process(i.directory_name,i.file_name,proj_id, num)

		
def filter_aoi(file,filename,proj_id):
	stimuli_data = Stimuli.query.filter_by(project_id=proj_id).first()
	stimuli_id = stimuli_data.stimuli_id
	aoi = Aoi.query.filter_by(stimuli_id=stimuli_id).all()
	y = []
	for b in range(len(aoi)):
		with open(file, 'r') as csv_file:
			reader = csv.reader(csv_file, delimiter=',')
			next(reader)
			for row in reader:
				if (int(row[0]) in range(aoi[b].x1, aoi[b].x2)) and (int(row[1]) in range(aoi[b].y1, aoi[b].y3)):
					print row[0], row[1]    
					line = str(reader.line_num)
					print type(line)
					line = re.findall(r'\d+', line)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
					y.append([int(row[0]), int(row[1]), aoi[b].new_id, (line)])
				elif IndexError:
					pass
				else:                                                                                                       
					print 'no match'
	with open(file, 'w') as new_file:
		file = csv.writer(new_file)
		for d in range(len(y)):
			file.writerow([(y[d])])
	
def clean_data(file,filename,proj_id):
	array = [] 
	with open(file,'r') as csv_file:
		reader = csv.reader(csv_file)
		for row in reader:
			print row
			for col in row:
				str1 = col.replace(']','').replace('[','')
				str1 = col.replace(']','').replace('[','')
				str1 = re.findall(r'\w+', str1) 
				array.append(str1[-2:])
				print array
	with open(file,'w') as read_file:
		writer = csv.writer(read_file)
		writer.writerows(array)
	with open(file, 'r') as csv_file:
		reader = csv.reader(csv_file)
		print array
		sort = sorted(array, key = lambda x: int(x[1]))
		with open(file, 'w') as read_file:
			writer = csv.writer(read_file)
			writer.writerows(sort)

def final_preprocess(file,filename,proj_id):
	array = []
	new_array = []
	with open(file,'r') as read_file:
		reader = csv.reader(read_file)
		for row in reader:
			array.append(row[0])
		for eachline in array[:]:
			for i in range(len(array)):
				try:
					if (int(array[i+1]) == int(array[i])):
						del array[i]
					else:
						pass
				except IndexError:
					break

	with open(file,'w') as write_file:
		print 'ey'
		writer = csv.writer(write_file)
		print 'ola'
		for i in range(len(array)):
			new_array.append(chr(int(array[i])))
			print chr(int(array[i]))
		writer.writerows(new_array)


def matrix(a, b, match_score=3, gap_cost=2):
	H = np.zeros((len(a) + 1, len(b) + 1), np.int)

	for i, j in itertools.product(range(1, H.shape[0]), range(1, H.shape[1])):
		match = H[i - 1, j - 1] + (match_score if a[i - 1] == b[j - 1] else - match_score)
		delete = H[i - 1, j] - gap_cost
		insert = H[i, j - 1] - gap_cost
		H[i, j] = max(match, delete, insert, 0)
	return H

def traceback(H, b, b_='', old_i=0):
	# flip H to get index of **last** occurrence of H.max() with np.argmax()
	H_flip = np.flip(np.flip(H, 0), 1)
	i_, j_ = np.unravel_index(H_flip.argmax(), H_flip.shape)
	i, j = np.subtract(H.shape, (i_ + 1, j_ + 1))  # (i, j) are **last** indexes of H.max()
	if H[i, j] == 0:
		return b_, j
	b_ = b[j - 1] + '-' + b_ if old_i - i > 1 else b[j - 1] + b_
	return traceback(H[0:i, 0:j], b, b_, i)

def smith_waterman(a, b, match_score=3, gap_cost=2):
	# a, b = a.upper(), b.upper()
	H = matrix(a, b, match_score, gap_cost)
	b_, pos = traceback(H, b)
	return pos, pos + len(b_)


def process(file, filename, proj_id, num):
	base_loc = upload_folder + '/' + str(current_user.researcher_id) + '/' + str(proj_id)
	arr = []
	dictionary = {}
	new_array = []
	temp_array = []
	temp_var = ''

	with open(file,'r') as read_file:
		reader = csv.reader(read_file)
		for row in reader:
			arr.append(row[0])

	with open(base_loc+'/preprocessed.csv','a') as write_file:
		writer = csv.writer(write_file)
		data = ''.join(map(str, arr))
		new_array.extend([num,data])
		writer.writerows([new_array])
	with open(base_loc+'/preprocessed.csv','r') as read:
		arrr = []
		permutes = []
		reader = csv.reader(read)
		for row in reader:
			arrr.append((row[0],row[1]))
		print arrr
		perm = combinations(arrr,2)
	with open(base_loc+'/permutations_result.csv','w') as perm_result:
		writer = csv.writer(perm_result)
		for i in (perm): 
			permutes.append(i)
			print i
			print permutes
			item1 = re.sub(r'[^A-Za-z]', '', str(i[0])) 
			item2 = re.sub(r'[^A-Za-z]', '', str(i[1])) 
			print matrix(item1,item2)
			print(smith_waterman(item1, item2))
			a, b = item1, item2
			H = matrix(a, b)
			result = traceback(H,b)
			dictionary.update({i: traceback(H,b)})
			print dictionary
			for key, value in dictionary.items():
				print key, value
				writer.writerow([key, value])
	with open(base_loc+'/permutations_result.csv','r') as csv_file:
		reader = csv.reader(csv_file)
		for row in reader:
			for i in range(len(row)): 
					temp_array.append(row[1])
	for i in range(len(temp_array)-1):

		if len(temp_array[i]) > len(temp_array[i+1]):
			temp_var = temp_array[i]
		else:
			temp_var = temp_array[i+1]
	with open(base_loc+'/preprocessed.csv','r') as csv_file:
		reader = csv.reader(csv_file)
		with open(base_loc+'/processed.csv','a') as write_file:
			writer = csv.writer(write_file)
			for row in reader:
				result = re.sub(r'[^A-Za-z]', '', str(temp_var)) 
				data = re.sub(r'[^A-Za-z]', '', str(row)) 
				print(smith_waterman(result, data))
				a, b = result, data
				print result,data
				H = matrix(a, b)
				temp_var = traceback(H,b)
				print temp_var
				if result != "":
					writer.writerow([a,b])
					writer.writerow(temp_var)
			return temp_var

@app.route('/<int:proj_id>/visualize',methods=['GET','POST'])
def visualize(proj_id):
	sequences = postprocess(proj_id)
	stimuli_data = Stimuli.query.filter_by(project_id=proj_id).first()
	filename = stimuli_data.stimuli_name 
	ext = filename.split('.')[-1]

	return render_template('project/visualize.html', x_res=stimuli_data.x_resolution,y_res=stimuli_data.y_resolution,\
		ext=ext,imgdata=stimuli_data.upload,sequences=sequences)

def postprocess(proj_id):
	stimuli_data = Stimuli.query.filter_by(project_id=proj_id).first()
	stimuli_id = stimuli_data.stimuli_id
	base_loc = upload_folder + '/' + str(current_user.researcher_id) + '/' + str(proj_id)
	arr = []
	new_array = []
	final_seq = ''
	with open(base_loc+'/processed.csv') as read_file:
		reader = csv.reader(read_file)
		for row in reader:
			arr.append(row)
	for i in arr[:]:
		final_seq = re.sub(r'[^A-Za-z]', '', str(arr[-1])) 
	for c in final_seq:
		new_array.append(Aoi.query.filter_by(stimuli_id=stimuli_id,new_id=ord(c)).first())
	print new_array		
	latest_array = [[(data.width-((data.x1+data.x2)/2)),(data.height-((data.y1+data.y3)/2))] for data in new_array]
	print latest_array
	return latest_array


@app.route('/<int:proj_id>/define/aoi', methods=['GET','POST'])
def save_aoi(proj_id):
	data = request.get_json()
	stimuli_data = Stimuli.query.filter_by(project_id=proj_id).first()
	filename = stimuli_data.stimuli_name 
	ext = filename.split('.')[-1]
	new_id = 65

	if request.method == 'POST':
		for i in range(len(data['startX'])-1):
			print i
			save_aoi =  Aoi(
				x1 = data['startX'][i],
				y1 = data['startY'][i],
				x2 = data['endX'][i],
				y2 = data['startY'][i],
				x3 = data['startX'][i],
				y3 = (data['endY'][i]),
				x4 = data['endX'][i],
				y4 = (data['endY'][i]),
				height = data['height'][i],
				width = data['width'][i],
				stimuli_id = stimuli_data.stimuli_id,
				new_id = new_id + i
				)

			db.session.add(save_aoi)
			db.session.commit()
		caller(proj_id)
		return redirect(url_for('analyse', proj_id=proj_id))
	return render_template('project/define_aoi.html', ext=ext, imgdata=stimuli_data.upload, proj_id=proj_id)

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

@app.route('/settings', methods=['POST','GET'])
def settings():
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
	return render_template('settings.html', form=form, user=user)

@app.route('/edit_profile')
def editprofile():
	return render_template('profile/edit_profile.html')

@app.route('/logout')
@login_required
def logout():
	session.clear()
	logout_user()
	return redirect(url_for('index'))

