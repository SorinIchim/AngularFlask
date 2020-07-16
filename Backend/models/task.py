import os, sys
import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from __init__ import db

class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	user = db.relationship("User", backref=db.backref("user", uselist=False), foreign_keys=[user_id])

	due_date = db.Column(db.DateTime())
	inceputM = db.Column(db.Integer())
	inceputH = db.Column(db.Integer())
	finalM = db.Column(db.Integer())
	finalH = db.Column(db.Integer())
	persons_nr = db.Column(db.Integer)
	biliard = db.Column(db.Integer, default=0)
	bowling = db.Column(db.Integer, default=0)
	darts = db.Column(db.Integer, default=0)

	description = db.Column(db.Text)

	comments = db.relationship("Comment", backref=db.backref("task"), lazy="dynamic")

	is_closed = db.Column(db.Boolean)
	created_at = db.Column(db.DateTime(), default=datetime.datetime.now)
	updated_at = db.Column(db.DateTime(), default=datetime.datetime.now)

	def __init__(self, title, user_id, persons_nr,inceputM, inceputH, finalH, finalM, 
	biliard=0, bowling=0, darts=0, description=None, due_date=None, 
	is_closed=False, created_at=datetime.datetime.now(), updated_at=datetime.datetime.now()):
		self.title = title
		self.persons_nr=persons_nr
		self.biliard=biliard
		self.bowling=bowling
		self.darts=darts
		self.description = None if description == '' else description
		self.user_id = user_id
		self.due_date = due_date
		self.inceputM = 0 if inceputM == '0' else inceputM
		self.inceputH = inceputH
		self.finalH = finalH
		self.finalM = 0 if finalM == '0' else finalM
		self.is_closed = is_closed
		self.created_at = created_at
		self.updated_at = updated_at

	def __repr__(self):
		return '<Task %r>' % self.title
