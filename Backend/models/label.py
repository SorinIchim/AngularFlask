import os, sys
import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from __init__ import db

class Label(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	color = db.Column(db.String(12))
	created_at = db.Column(db.DateTime(), default=datetime.datetime.now)
	updated_at = db.Column(db.DateTime(), default=datetime.datetime.now)

	def __init__(self, name, color):
		self.name = name
		self.color = color

	def __repr__(self):
		return '<Label %r>' % self.name
