import os
from __init__ import app

SECRET_KEY = 'secret-key'
DEBUG = True
DB_USERNAME = ''
DB_PASSWORD = ''
TASK_DATABASE_NAME = ''
DB_HOST = os.getenv('IP', '127.0.0.1')
DB_URI = "mysql+pymysql://%s:%s@%s/%s" % (DB_USERNAME, DB_PASSWORD, DB_HOST, TASK_DATABASE_NAME)
SQLALCHEMY_DATABASE_URI = DB_URI

app.config["IMAGE_UPLOADS"] = "static/img/uploads"
