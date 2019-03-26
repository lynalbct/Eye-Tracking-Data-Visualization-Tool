import os
import secrets
from PIL import Image
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
	return render_template('landing/index.html')

@app.route('/forgotpassword')
def forgotpassword():
	return render_template('dashboard/forgot-password.html')

@app.route('/prof')
def prof():
	return render_template('profile/profile.html')
@app.route('/stimuli')
def stimuli():
	return render_template('stimuli/stimuli.html')

@app.route('/log')
def log():
	form = LoginForm()
	# if current_user.is_authenticated is True:
	# 	return redirect(url_for('home'))
	if form.validate_on_submit():
		user = Researcher.query.filter_by(username=form.username.data).first()
		if user:
			print(form.password.data)
			if check_password_hash(user.password, form.password.data):
				login_user(user, remember=True)
				return redirect(url_for('home'))
			else:
				flash('Invalid username or password')
				return render_template('dashboard/login.html', form=form)
		else:
			return render_template('dashboard/login.html', form=form)
	return render_template('dashboard/login.html', form=form)

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
				return redirect(url_for('home'))
			else:
				flash('Invalid username or password')
				return render_template('dashboard/login.html', form=form)
		else:
			return render_template('dashboard/login.html', form=form)
	return render_template('dashboard/login.html', form=form)

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
			db.session.add(new_user)
			db.session.commit()
			if new_user is True:
				login_user(new_user, remember=True)
				return redirect(url_for('info'))
			return redirect(url_for('info'))
		else:
			return redirect(url_for('register'))
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
	image_file = url_for('static', filename='images/' + current_user.image_file)
	res = Researcher.query.filter_by(researcher_id =current_user.researcher_id).first()
	return render_template('index.html', image_file=image_file, res=res)

@app.route('/profile/<int:researcher_id>', methods=['POST','GET'])
def profile(researcher_id):
	image_file = url_for('static', filename='images/' + current_user.image_file)
	res = Researcher.query.filter_by(researcher_id = current_user.researcher_id).first()
	form = ProfileForm()
	print(form)
	user = Researcher.query.filter_by(researcher_id =current_user.researcher_id)
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
	return render_template('profile.html', image_file=image_file, form=form, res=res)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/profile/edit/<int:researcher_id>', methods=['POST','GET'])
@login_required
def profile_edit(researcher_id):
    form = UpdateAccountForm()
    if form.validate_on_submit():
    	if form.picture.data:
    		picture_file = save_picture(form.picture.data)
    		current_user.image_file = picture_file
    	current_user.first_name = form.first_name.data
    	current_user.last_name = form.last_name.data
    	current_user.username = form.username.data
    	current_user.email = form.email.data
    	current_user.profession = form.profession.data
    	current_user.organization = form.organization.data
    	db.session.commit()
    	flash('Your account has been updated!', 'success')
    	res = Researcher.query.filter_by(researcher_id=current_user.researcher_id).first()
    	return render_template('profile-edit.html', res=res, form=form, researcher_id=current_user.researcher_id)
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.profession.data = current_user.profession
        form.organization.data = current_user.organization
        image_file = url_for('static', filename='images/' + current_user.image_file)
        res = Researcher.query.filter_by(researcher_id=current_user.researcher_id).first()
    return render_template('profile-edit.html', res = res, form = form, image_file=image_file, title = "Account")

@app.route('/connections/<researcher_id>')
@login_required
def connections(researcher_id):
	image_file = url_for('static', filename='images/' + current_user.image_file)
	res = Researcher.query.filter_by(researcher_id=researcher_id).first()
	posts = [
        {'author': res, 'body': 'Test post #1'},
        {'author': res, 'body': 'Test post #2'}
    ]
	return render_template('connections.html', res=res, posts=posts, image_file=image_file)

@app.route('/connections/search/<researcher_id>')
@login_required
def connections_search(researcher_id):
	image_file = url_for('static', filename='images/' + current_user.image_file)
	res = Researcher.query.filter_by(researcher_id=current_user.researcher_id).first()
	return render_template('connections-search.html', res=res, image_file=image_file)

@app.route('/follow/<researcher_id>')
@login_required
def follow(researcher_id):
    res = Researcher.query.filter_by(researcher_id=researcher_id).first()
    if res is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('home'))
    if res == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('connections', researcher_id=researcher_id))
    current_user.follow(res)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('connections', researcher_id=researcher_id))


@app.route('/unfollow/<researcher_id>')
@login_required
def unfollow(researcher_id):
    res = Researcher.query.filter_by(researcher_id=researcher_id).first()
    if res is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('home'))
    if res == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('connections', researcher_id=researcher_id))
    current_user.unfollow(res)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('connections', researcher_id=researcher_id))

@app.route('/projects/<int:researcher_id>')
def projects(researcher_id):
	res = Researcher.query.filter_by(researcher_id =current_user.researcher_id).first()
	return render_template('projects.html', res= res, title="Title")
	



@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))

