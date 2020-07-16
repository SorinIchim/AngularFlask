import os, sys
import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from __init__ import db

class Produs(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	price = db.Column(db.Float())
	stock = db.Column(db.Integer())

	def __init__(self, name, price, stock):
		self.name = name
		self.price = price
		self.stock = stock

	def __repr__(self):
		return '<Produs %r>' % self.name
