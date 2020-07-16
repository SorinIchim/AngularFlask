from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config.from_object('settings')
db = SQLAlchemy(app)

from user import views
from task import views
from tarife import views
