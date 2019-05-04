from app import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from flask_table import Table, Col


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('researcher.researcher_id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('researcher.researcher_id'))
)


class Researcher(UserMixin, db.Model):
	__tablename__ = 'researcher'
	researcher_id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(140))
	last_name = db.Column(db.String(140))
	username = db.Column(db.String(140))
	profession = db.Column(db.String(140))
	organization = db.Column(db.String(140))
	email = db.Column(db.String(140), nullable=False, unique=True)
	password = db.Column(db.String(140), nullable=False)
	date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	connections = db.relationship("Connection", uselist=False, backref="researcher")
	projects = db.relationship("Project", uselist=False, backref="researcher")
	sharedprojects = db.relationship("SharedProject", uselist=False, backref="researcher")
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	followed = db.relationship(
        'Researcher', secondary=followers,
        primaryjoin=(followers.c.follower_id == researcher_id),
        secondaryjoin=(followers.c.followed_id == researcher_id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
	

	def __init__(self, username='', email='',password=''):
		self.first_name = ''
		self.last_name = ''
		self.username = username
		self.profession = ''
		self.organization = ''
		self.email = email
		self.password = generate_password_hash(password, method='sha256')


	def get_id(self):
		return (self.researcher_id)

	def isAuthenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False
	
	def follow(self, researcher):
		if not self.is_following(researcher):
			self.followed.append(researcher)

	def unfollow(self, researcher):
		if self.is_following(researcher):
			self.followed.remove(researcher)
	
	def is_following(self, researcher):
		return self.followed.filter(
			followers.c.followed_id == researcher.researcher_id).count() > 0
		
	def __repr__(self):
		return '<Researcher %r>' % self.researcher_id 


class File(db.Model):
	__tablename__ = 'file'
	file_id = db.Column(db.Integer, primary_key = True)
	file_name = db.Column(db.String(80))
	file_type = db.Column(db.String(50))
	directory_name = db.Column(db.String(80))
	file_extension = db.Column(db.String(50))
	researcher_id = db.Column(db.Integer, db.ForeignKey('researcher.researcher_id'))
	"""docstring for Files"""
	def __init__(self, file_id,file_name,file_type,file_extension,directory_name,researcher_id):
		self.file_id = file_id
		self,file_name = file_name
		self.file_type = file_type
		self.file_extension = file_extension
		self.directory_name = directory_name
		self.researcher_id = researcher_id

	def __repr__(self):
		return 'File %r' % self.file_id

class Connection(db.Model):
	__tablename__ = 'connection'
	connections_id = db.Column(db.Integer, primary_key=True)
	status = db.Column('status', db.String())
	anonymousuest = db.Column(db.DateTime, default=datetime.utcnow)
	date_accepted = db.Column(db.DateTime)
	request_id = db.Column(db.Integer)
	researcher_id = db.Column(db.Integer, db.ForeignKey('researcher.researcher_id'))
	
	def __init__(self,status,date_accepted,request_id,researcher_id):
		self.status = status
		self.date_accepted = date_accepted
		self.request_id = request_id
		self.researcher_id = researcher_id
	

	def __repr__(self):
		return '<Researcher %r>' % self.connections_id

class Results(Table):
	researcher_id = Col('researcher_id')
	first_name = Col('First Name')
	last_name = Col('Last Name')
	username = Col('Username')
	email = Col('Email Address')
	profession = Col('Profession')
	organization = Col('Organization')


class Request(Table):
	connections_id = Col('connections_id', show=False)
	request_id = Col('request_id')
	Researcher.first_name = Col('first name')
	status = Col('status')


class Project(db.Model):
	__tablename__ = 'project'	
	project_id = db.Column(db.Integer, primary_key=True)
	project_name = db.Column(db.String(140), nullable = False)
	project_description = db.Column(db.String(200))
	date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	date_modified = db.Column(db.DateTime, nullable=False)
	row_status = db.Column(db.Integer)
	researcher_id = db.Column(db.Integer, db.ForeignKey('researcher.researcher_id'))
	sharedprojects = db.relationship("SharedProject", uselist=False, backref="project")
	stimuli = db.relationship("Stimuli", uselist=False, backref="project")

	def __init__(self, project_name,project_description,date_modified,row_status,researcher_id):
		self.project_name = project_name
		self.project_description = project_description
		self.date_modified = date_modified
		self.row_status = row_status
		self.researcher_id = researcher_id
		
	def __repr__(self):
		return 'Project %r' % self.project_id

class SharedProject(db.Model):
	__tablename__ = 'sharedproject'
	sharedproject_id = db.Column(db.Integer, primary_key=True)
	status = db.Column(db.Integer, default=0)
	sp_date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
	sp_date_modified = db.Column(db.DateTime)
	shared_to = db.Column(db.Integer)
	researcher_id = db.Column(db.Integer, db.ForeignKey('researcher.researcher_id'))
	project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'))

	def __init__(self, status, sp_date_modified, shared_to, researcher_id,project_id ):
		self.status = status
		self.sp_date_modified = sp_date_modified
		self.shared_to = shared_to
		self.researcher_id = researcher_id
		self.project_id = project_id

	def __repr__(self):
		return 'SharedProject %r' % self.sharedproject_id

class Stimuli(db.Model):
	__tablename__ = 'stimuli'
	stimuli_id = db.Column(db.Integer, primary_key=True)
	stimuli_name = db.Column(db.String(80))
	stimuli_description = db.Column(db.String(120))
	x_resolution = db.Column(db.Integer, nullable=False)
	y_resolution = db.Column(db.Integer, nullable=False)
	date_created = db.Column(db.DateTime, default = datetime.utcnow, nullable=False)
	date_modified = db.Column(db.DateTime)
	project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'))
	stimuli_participant = db.relationship("Stimuli_Participant", uselist=False, backref="stimuli")
	aoi = db.relationship("Aoi", uselist=False, backref="stimuli")

	def __init__(self, stimuli_name, stimuli_description,x_resolution,y_resolution,date_modified,project_id):
		self.stimuli_name = stimuli_name
		self.stimuli_description = stimuli_description
		self.x_resolution = x_resolution
		self.y_resolution = y_resolution
		self.date_modified = date_modified
		self.project_id = project_id

	def __repr__(self):
		return 'Stimuli %r' % self.stimuli_id

class Participant(db.Model):
	__tablename__ = 'participant'
	participant_id = db.Column(db.Integer,primary_key=True)
	participant_name = db.Column(db.String(80))
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	date_modified = db.Column(db.DateTime)
	stimuli_participant = db.relationship("Stimuli_Participant", uselist=False, backref="participant")
	fixation_analysis = db.relationship("Fixation_Analysis", uselist=False, backref="participant")
	
	def __init__(self,participant_name,date_modified):
		self.participant_name = participant_name
		self.date_modified = date_modified

	def __repr__(self):
		return 'Participant %r' %self.participant_id


class Stimuli_Participant(db.Model):
	stimuli_participant_id = db.Column(db.Integer, primary_key=True)
	stimuli_id = db.Column(db.Integer, db.ForeignKey('stimuli.stimuli_id'))
	participant_id = db.Column(db.Integer, db.ForeignKey('participant.participant_id'))

	def __init__(self, stimuli_id,participant_id):
		self.stimuli_id = stimuli_id
		self.participant_id = participant_id

	def __repr__(self):
		return 'Stimuli_Participant %r' %self.stimuli_participant_id

class Aoi(db.Model):
	__tablename__ = 'aoi'
	aoi_id = db.Column(db.Integer, primary_key=True)
	x1 = db.Column(db.Integer)
	y1 = db.Column(db.Integer)
	x2 = db.Column(db.Integer)
	y2 = db.Column(db.Integer)
	x3 = db.Column(db.Integer)
	y3 = db.Column(db.Integer)
	x4 = db.Column(db.Integer)
	y4 = db.Column(db.Integer)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	date_modified = db.Column(db.DateTime)
	stimuli_id = db.Column(db.Integer, db.ForeignKey('stimuli.stimuli_id'))
	fixation_analysis = db.relationship("Fixation_Analysis", uselist=False, backref="aoi")

	def __init__(self,x1,y1,x2,y2,x3,y3,x4,y4,date_modified, stimuli_id):
		self.x1 =x1
		self.y1 =y1
		self.x2 =x2
		self.y2 =x1
		self.x3 =x3
		self.y3 =y3
		self.x4 =x4
		self.y4 =y4
		self.date_modified =date_modified
		self.stimuli_id=stimuli_id
	def __repr__(self):
		return 'Aoi %r' % self.aoi_id

class Fixation_Analysis(db.Model):
	__tablename__ = 'fixation_analysis'
	fixation_analysis_id = db.Column(db.Integer, primary_key=True)
	nof = db.Column(db.Integer)
	dff = db.Column(db.Integer)
	tct = db.Column(db.Integer)
	date_created = db.Column(db.DateTime, default = datetime.utcnow)
	date_modified = db.Column(db.DateTime)
	aoi_id = db.Column(db.Integer, db.ForeignKey('aoi.aoi_id'))
	participant_id = db.Column(db.Integer, db.ForeignKey('participant.participant_id'))

	def __init__(self,nof,dff,tct,date_modified,aoi_id,participant_id):
		self.nof = nof
		self.dff = dff
		self.tct = tct
		self.date_modified = date_modified
		self.aoi_id = aoi_id
		self.participant_id = participant_id
	def __repr__(self):
		return 'Fixation_Analysis %r' % self.fixation_analysis_id

class Fixation(db.Model):
	__tablename__ = 'fixation'
	fixation_id = db.Column(db.Integer,primary_key=True)
	x = db.Column(db.Integer)
	y = db.Column(db.Integer)
	duration = db.Column(db.Integer)
	participant_id = db.Column(db.Integer, db.ForeignKey('participant.participant_id'))

	def __init__(self,x,y,duration,participant_id):
		self.x =x
		self.y =y
		self.duration = duration
		self.participant_id = participant_id
	def __repr__(self):
		return 'Fixation %r' %self.fixation_id





		
		
		
		
		
