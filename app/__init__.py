from flask import Flask, Blueprint, session
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *

import psycopg2


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/etdvt'
db = SQLAlchemy(app)

from app import config
from app import models
from app import server
app.debug = True


