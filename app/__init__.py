from flask import Flask, Blueprint, session
import os
import sys
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from flask_bootstrap import Bootstrap

import psycopg2


app = Flask(__name__)
Bootstrap(app)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/etdvt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'etdvt'

from app import models
from app import server
from app.server import upload_folder

app.config['UPLOAD_FOLDER'] = upload_folder


db.create_all()
app.debug = True


