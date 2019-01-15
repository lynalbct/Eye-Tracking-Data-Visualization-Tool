from flask import Flask, Blueprint, session
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
# from flask_mail import Mail
# from flask_script import Manager
# from flask_migrate import Migrate, MigrateCommand
import psycopg2
# from flask_compress import Compress
# from flask_marshmallow import Marshmallow


app = Flask(__name__)
# ma = Marshmallow(app)


# app.config['SECRET_KEY'] = 'hard to guess string'
# app.config['CORS_HEADERS'] = "Content-Type, Authorization"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# mail = Mail(app)
# Compress(app)

from app import server
# manager = Manager(app)
app.debug = True


