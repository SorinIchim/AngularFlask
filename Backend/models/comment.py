import os, sys
import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from __init__ import db

class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	usercomm = db.relationship("User", backref=db.backref("usercomm", uselist=False), foreign_keys=[user_id])
	body = db.Column(db.Text)
	date = db.Column(db.DateTime())

	def __init__(self, task_id, comment_user_id, comment_body, comment_date):
		self.task_id = task_id
		self.user_id = comment_user_id
		self.body = comment_body
		self.date = comment_date

	def __repr__(self):
		return f'''
			Comment {self.id}
			-----------------
			User ID: {self.user_id}
			Body: {self.body}
			Date: {self.date}
		'''
