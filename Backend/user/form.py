from flask_wtf import Form
from wtforms import validators, StringField, PasswordField, FileField
from wtforms.fields.html5 import EmailField
from flask_wtf.file import FileAllowed

class RegisterForm(Form):
	image = FileField("Image", validators=[
		FileAllowed(['jpg', 'png'], 'We only accept JPG or PNG images')
		])
	fullname = StringField('Full Name', [validators.Required()])
	email = EmailField('Email', [validators.Required()])
	username = StringField('Username', [
		validators.Required(),
		validators.Length(min=4, max=25)
		])
	password = PasswordField('Password', [
		validators.Required(),
		validators.EqualTo('confirm', message="Password must match"),
		validators.Length(min=4, max=80)
		])
	confirm = PasswordField('Repeat Password')

class LoginForm(Form):
	username = StringField('Username', [
		validators.Required(),
		validators.Length(min=4, max=25)
		])
	password = PasswordField('Password', [
		validators.Required(),
		validators.Length(min=4, max=80)
		])
