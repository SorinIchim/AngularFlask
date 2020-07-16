from flask_wtf import Form
from wtforms import validators, StringField, PasswordField, TextAreaField, DateTimeField, DecimalField, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
import datetime
from models.user import User
from models.label import Label

def user():
	return User.query
	
def label():
	return Label.query

class TaskForm(Form):
	title = StringField('Title', [validators.Required()])
	description = TextAreaField('Description')
	biliard = DecimalField('biliard')
	bowling = DecimalField('bowling')
	darts = DecimalField('darts')
	persons_nr = IntegerField('persons_nr')
	inceputH = IntegerField('inceputH')
	inceputM = IntegerField('inceputM')
	finalH = IntegerField('finalH')
	finalM = IntegerField('finalM')

class LabelForm(Form):
	name = StringField('name', [validators.Required(),
		validators.Length(min=4, max=80)
		])
	color = StringField('color', [validators.Required()])

class CommentForm(Form):
	comment_body = TextAreaField('Comment Body', [validators.Required()])
