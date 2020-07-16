from functools import wraps
from flask import session, request, redirect, url_for, abort

def login_required(f):
	@wraps(f)
	def decorade_function(*args, **kwargs):
		if session.get('username') is None:
			return redirect(url_for('login', next=request.url))
		return f(*args, **kwargs)
	return decorade_function
	
def admin(f):
	@wraps(f)
	def decorade_function(*args, **kwargs):
		if session.get('is_admin')!="True":
			return redirect(url_for('index', next=request.url))
		return f(*args, **kwargs)
	return decorade_function

def anti_login(f):
	@wraps(f)
	def decorade_function(*args, **kwargs):
		if session.get('username'):
			return redirect(url_for('index', next=request.url))
		return f(*args, **kwargs)
	return decorade_function