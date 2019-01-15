from flask import Flask, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, url_for,redirect,send_from_directory
from app import app
from flask import render_template, request, url_for,redirect,send_from_directory
# import requests
# import os
# from werkzeug.security import generate_password_hash, check_password_hash
# import sys, flask, requests
# from flask_marshmallow import Marshmallow
# from flask_cors import CORS, cross_origin
# from SimpleHTTPServer import SimpleHTTPRequestHandler, test




@app.route('/')
def index():
	return render_template('landing/index.html')