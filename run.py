from flask import Flask
import os
from app import app



if __name__ == '__main__':
	app.run(host='localhost',port=8000, threaded = True)

	# port = int(os.environ.get("PORT", 8000))
	# app.run(host='0.0.0.0', port=port)

