from __init__ import app
from flask import render_template, redirect, url_for, flash, session, request, flash, abort
from user.form import RegisterForm, LoginForm
from task.form import TaskForm
from models.user import User
from __init__ import db
from user.decorators import login_required, anti_login
import bcrypt
import os

#==================================================================
#==============================LOGIN===============================
#==================================================================

@app.route('/login', methods=('GET', 'POST'))
@anti_login
def login():
	form = LoginForm()
	error = None

	if request.method == 'GET' and request.args.get('next'):
		session['next'] = request.args.get('next', None)

	if form.validate_on_submit():
		user = User.query.filter_by(
			username=form.username.data
			).first()
		if user:
			if bcrypt.hashpw(form.password.data, user.password) == user.password:
				session['user_id'] = user.id
				session['username'] = form.username.data
				session['has_avatar'] = os.path.exists(f'static/img/uploads/{user.id}.jpg')
				session['is_admin'] = format(user.is_admin)
				session['email'] = user.email
				flash("User %s logged in" % form.username.data)
				if 'next' in session:
					next = session.get('next')
					session.pop('next')
					return redirect(next)
				else:
					return redirect(url_for('index'))
			else:
				error = "Incorrect username and password"
				flash("Incorrect username and password")
		else:
			error = "Incorrect username and password"
			flash("Incorrect username and password")
	return render_template('user/login.html', form=form, error=error)

#==================================================================
#==============================REGISTER============================
#==================================================================

@app.route('/register', methods=('GET', 'POST'))
@anti_login
def register():
	directory = os.path.dirname(app.config["IMAGE_UPLOADS"])
	if not os.path.exists(directory):
		os.makedirs(directory)
		
	form = RegisterForm()
	if form.validate_on_submit():
		salt = bcrypt.gensalt()
		hashed_password = bcrypt.hashpw(form.password.data, salt)

		user = User(
			fullname = form.fullname.data,
			email = form.email.data,
			username = form.username.data,
			password = hashed_password
			)

		db.session.add(user)
		db.session.commit()

		image = request.files["image"]
		image.save(os.path.join(app.config["IMAGE_UPLOADS"], str(user.id) + ".jpg"))

		flash("User created")
		return redirect(url_for('login'))

	else:
		print(f"Form failed: {form.errors}")

	return render_template('user/register.html', form=form)

#==================================================================
#============================PROFILE===============================
#==================================================================

@app.route('/profile', methods=('GET', 'POST'))
def profile():
	user = User.query.filter_by(id=session['user_id']).first_or_404()	
	session["minuteBiliard"] = user.minuteBiliard
	session["minuteBowling"] = user.minuteBowling
	session["minuteDarts"] = user.minuteDarts
	session["minuteTotal"] = user.minuteBiliard + user.minuteBowling + user.minuteDarts

	session["nrBiliard"] = user.nrBiliard
	session["nrBowling"] = user.nrBowling
	session["nrDarts"] = user.nrDarts
	session["nrTotal"] = user.nrBiliard + user.nrBowling + user.nrDarts
	return render_template('user/profile.html')

#==================================================================
#============================CONTACT===============================
#==================================================================

@app.route('/contact')
def contact():
	return render_template('user/contact.html')

#==================================================================
#==============================ETC=================================
#==================================================================

@app.route('/logout')
def logout():
	session.pop('username')
	flash("User logged out")
	return redirect(url_for('login'))
