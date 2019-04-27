from app import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash



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
		
	def __repr__(self):
		return '<Researcher %r>' % self.researcher_id


class File(db.Model):
	__tablename__ = 'file'
	file_id = db.Column(db.Integer, primary_key = True)
	file_name = db.Column(db.String(80))
	directory_name = db.Column(db.String(80))
	researcher_id = db.Column(db.Integer, db.ForeignKey('researcher.researcher_id'))
	project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'))
	"""docstring for Files"""
	def __init__(self, file_name,directory_name,researcher_id, project_id):
		self.file_name = file_name
		self.directory_name = directory_name
		self.researcher_id = researcher_id
		self.project_id = project_id

	def __repr__(self):
		return 'File %r' % self.file_id

# class Connection(db.Model):
# 	__tablename__ = 'connection'
# 	connections_id = db.Column(db.Integer, primary_key=True)
# 	status = db.Column(db.Integer, default=0)
# 	date_request = db.Column(db.DateTime, default=datetime.utcnow)
# 	date_accepted = db.Column(db.DateTime)
# 	request_id = db.Column(db.Integer)
# 	researcher_id = db.Column(db.Integer, db.ForeignKey('researcher.researcher_id'))

# 	def __init__(self, researcher_id=''):
# 		self.status = None
# 		self.date_accepted = None
# 		self.request_id = None
# 		self.researcher_id = researcher_id

# 	def __repr__(self):
# 		return '<Researcher %r>' % self.connections_id

class Project(db.Model):
	__tablename__ = 'project'
	project_id = db.Column(db.Integer, primary_key=True)
	project_name = db.Column(db.String(140), nullable = False)
	project_description = db.Column(db.String(200))
	date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	researcher_id = db.Column(db.Integer, db.ForeignKey('researcher.researcher_id'))
	sharedprojects = db.relationship("SharedProject", uselist=False, backref="project")
	files = db.relationship("File", uselist=False, backref="project")
	stimuli = db.relationship("Stimuli", uselist=False, backref="project")

	def __init__(self, project_name,project_description,researcher_id):
		self.project_name = project_name
		self.project_description = project_description
		self.researcher_id = researcher_id
		
	def __repr__(self):
		return 'Project %r' % self.project_id

# class SharedProject(db.Model):
# 	__tablename__ = 'sharedproject'
# 	sharedproject_id = db.Column(db.Integer, primary_key=True)
# 	status = db.Column(db.Integer, default=0)
# 	sp_date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
# 	shared_to = db.Column(db.Integer)
# 	researcher_id = db.Column(db.Integer, db.ForeignKey('researcher.researcher_id'))
# 	project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'))

# 	def __init__(self, status, shared_to, researcher_id,project_id):
# 		self.status = status
# 		self.shared_to = shared_to
# 		self.researcher_id = researcher_id
# 		self.project_id = project_id

# 	def __repr__(self):
# 		return 'SharedProject %r' % self.sharedproject_id

class Stimuli(db.Model):
	__tablename__ = 'stimuli'
	stimuli_id = db.Column(db.Integer, primary_key=True)
	stimuli_name = db.Column(db.String(80))
	upload = db.Column(db.String(2000000))
	stimuli_description = db.Column(db.String(120))
	x_resolution = db.Column(db.Integer, nullable=False)
	y_resolution = db.Column(db.Integer, nullable=False)
	date_created = db.Column(db.DateTime, default = datetime.utcnow, nullable=False)
	project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'))
	stimuli_participant = db.relationship("Stimuli_Participant", uselist=False, backref="stimuli")
	aoi = db.relationship("Aoi", uselist=False, backref="stimuli")

	def __init__(self, stimuli_name,upload, stimuli_description,x_resolution,y_resolution,project_id):
		self.stimuli_name = stimuli_name
		self.upload = upload
		self.stimuli_description = stimuli_description
		self.x_resolution = x_resolution
		self.y_resolution = y_resolution
		self.project_id = project_id

	def __repr__(self):
		return 'Stimuli %r' % self.stimuli_id

# class Participant(db.Model):
# 	__tablename__ = 'participant'
# 	participant_id = db.Column(db.Integer,primary_key=True)
# 	participant_name = db.Column(db.String(80))
# 	date_created = db.Column(db.DateTime, default=datetime.utcnow)
# 	stimuli_participant = db.relationship("Stimuli_Participant", uselist=False, backref="participant")
# 	fixation_analysis = db.relationship("Fixation_Analysis", uselist=False, backref="participant")
	
# 	def __init__(self,participant_name):
# 		self.participant_name = participant_name

# 	def __repr__(self):
# 		return 'Participant %r' %self.participant_id


# class Stimuli_Participant(db.Model):
# 	stimuli_participant_id = db.Column(db.Integer, primary_key=True)
# 	stimuli_id = db.Column(db.Integer, db.ForeignKey('stimuli.stimuli_id'))
# 	participant_id = db.Column(db.Integer, db.ForeignKey('participant.participant_id'))

# 	def __init__(self, stimuli_id,participant_id):
# 		self.stimuli_id = stimuli_id
# 		self.participant_id = participant_id

# 	def __repr__(self):
# 		return 'Stimuli_Participant %r' %self.stimuli_participant_id

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
	stimuli_id = db.Column(db.Integer, db.ForeignKey('stimuli.stimuli_id'))
	new_id = db.Column(db.Integer)
	fixation_analysis = db.relationship("Fixation_Analysis", uselist=False, backref="aoi")

	def __init__(self,x1,y1,x2,y2,x3,y3,x4,y4, stimuli_id, new_id):
		self.x1 =x1
		self.y1 =y1
		self.x2 =x2
		self.y2 =x1
		self.x3 =x3
		self.y3 =y3
		self.x4 =x4
		self.y4 =y4
		self.stimuli_id=stimuli_id
		self.new_id=new_id

	def __repr__(self):
		return 'Aoi %r' % self.aoi_id

# class Fixation_Analysis(db.Model):
# 	__tablename__ = 'fixation_analysis'
# 	fixation_analysis_id = db.Column(db.Integer, primary_key=True)
# 	nof = db.Column(db.Integer)
# 	dff = db.Column(db.Integer)
# 	tct = db.Column(db.Integer)
# 	date_created = db.Column(db.DateTime, default = datetime.utcnow)
# 	aoi_id = db.Column(db.Integer, db.ForeignKey('aoi.aoi_id'))
# 	participant_id = db.Column(db.Integer, db.ForeignKey('participant.participant_id'))

# 	def __init__(self,nof,dff,tct,aoi_id,participant_id):
# 		self.nof = nof
# 		self.dff = dff
# 		self.tct = tct
# 		self.aoi_id = aoi_id
# 		self.participant_id = participant_id
# 	def __repr__(self):
# 		return 'Fixation_Analysis %r' % self.fixation_analysis_id

# class Fixation(db.Model):
# 	__tablename__ = 'fixation'
# 	fixation_id = db.Column(db.Integer,primary_key=True)
# 	x = db.Column(db.Integer)
# 	y = db.Column(db.Integer)
# 	duration = db.Column(db.Integer)
# 	participant_id = db.Column(db.Integer, db.ForeignKey('participant.participant_id'))

# 	def __init__(self,x,y,duration,participant_id):
# 		self.x =x
# 		self.y =y
# 		self.duration = duration
# 		self.participant_id = participant_id
# 	def __repr__(self):
# 		return 'Fixation %r' %self.fixation_id





		
		
		
		
		
