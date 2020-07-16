import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from __init__ import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	fullname = db.Column(db.String(80))
	email = db.Column(db.String(35), unique = True)
	username = db.Column(db.String(80), unique = True)
	password = db.Column(db.String(80))
	is_admin = db.Column(db.Boolean(), default = False)
	minuteBiliard = db.Column(db.Integer(), default = 0)
	minuteBowling = db.Column(db.Integer(), default = 0)
	minuteDarts = db.Column(db.Integer(), default = 0)
	minuteTotal = db.Column(db.Integer(), default = 0)
	nrBiliard = db.Column(db.Integer(), default = 0)
	nrBowling = db.Column(db.Integer(), default = 0)
	nrDarts = db.Column(db.Integer(), default = 0)
	nrTotal = db.Column(db.Integer(), default = 0)
	nrPuncte = db.Column(db.Integer(), default = 0)

	def __init__(self, fullname, email, username, password,
	minuteBiliard=0, minuteBowling=0, minuteDarts=0, minuteTotal=0, nrBiliard=0, nrBowling=0, nrDarts=0, nrTotal=0, nrPuncte=0,
	is_admin=False):
		self.fullname = fullname
		self.email = email
		self.username = username
		self.password = password
		self.is_admin = is_admin
		self.minuteBiliard = minuteBiliard
		self.minuteBowling = minuteBowling
		self.minuteDarts = minuteDarts
		self.minuteTotal = minuteTotal
		self.nrBiliard = nrBiliard
		self.nrBowling = nrBowling
		self.nrDarts = nrDarts
		self.nrTotal = nrTotal
		self.nrPuncte = nrPuncte 

	def __repr__(self):
		return '<User %r>' % self.username
