from __init__ import app
from flask import render_template, redirect, url_for, flash, session, abort, request
from task.form import LabelForm, TaskForm, CommentForm
from user.form import RegisterForm
from __init__ import db
from models.task import Task
from models.label import Label
from models.user import User
from models.comment import Comment
from user.decorators import login_required, admin
import datetime
from slugify import slugify
import os

# =========================================================================
# ==============================TASKS LIST=================================
# =========================================================================

# @app.route('/')
# @app.route('/index')
# def index(page=1):
# 	return render_template('task/index.html')

@app.route('/tasks')
@app.route('/tasks/<int:page>')
@login_required
def tasks(page=1):
	task = Task.query.all()
	if not task:
		return redirect(url_for('task'))
	tasks = Task.query.order_by(Task.due_date.asc()).order_by(Task.inceputH.asc()).order_by(Task.inceputM.asc()).paginate(page, app.config['ITEMS_PER_PAGE'], False)
	return render_template('task/tasks.html', tasks=tasks)
	
@app.route('/tasks/session')
@login_required
def sessiontasks(page=1):
	tasks = Task.query.filter_by(user_id = session['user_id']).order_by(Task.due_date.asc()).order_by(Task.inceputH.asc()).order_by(Task.inceputM.asc()).paginate(page, app.config['ITEMS_PER_PAGE'], False)
	if not tasks:
		return redirect(url_for('task'))
	return render_template('task/tasks.html', tasks=tasks)

@app.route('/tasks/open')
@login_required
def opentasks(page=1):
	tasks = Task.query.filter_by(is_closed = 0).order_by(Task.due_date.asc()).order_by(Task.inceputH.asc()).order_by(Task.inceputM.asc()).paginate(page, app.config['ITEMS_PER_PAGE'], False)
	return render_template('task/tasks.html', tasks=tasks)

@app.route('/tasks/closed')
@login_required
def closedtasks(page=1):
	tasks = Task.query.filter_by(is_closed = 1).order_by(Task.due_date.asc()).order_by(Task.inceputH.asc()).order_by(Task.inceputM.asc()).paginate(page, app.config['ITEMS_PER_PAGE'], False)
	return render_template('task/tasks.html', tasks=tasks)

@app.route('/tasks/biliard')
@login_required
def biliardtasks(page=1):
	tasks = Task.query.filter (Task.biliard != 0).order_by(Task.due_date.asc()).order_by(Task.inceputH.asc()).order_by(Task.inceputM.asc()).paginate(page, app.config['ITEMS_PER_PAGE'], False)
	return render_template('task/tasks.html', tasks=tasks)

@app.route('/tasks/bowling')
@login_required
def bowlingtasks(page=1):
	tasks = Task.query.filter (Task.bowling != 0).order_by(Task.due_date.asc()).order_by(Task.inceputH.asc()).order_by(Task.inceputM.asc()).paginate(page, app.config['ITEMS_PER_PAGE'], False)
	return render_template('task/tasks.html', tasks=tasks)

@app.route('/tasks/darts')
@login_required
def dartstasks(page=1):
	tasks = Task.query.filter (Task.darts != 0).order_by(Task.due_date.asc()).order_by(Task.inceputH.asc()).order_by(Task.inceputM.asc()).paginate(page, app.config['ITEMS_PER_PAGE'], False)
	return render_template('task/tasks.html', tasks=tasks)

# =========================================================================
# ==============================TASK=======================================
# =========================================================================
@app.route('/task', methods=('GET', 'POST'))
@login_required
def task():

	form = TaskForm()
	if form.validate_on_submit():
		title = form.title.data
		task = Task(
			title = title, 
			user_id = session['user_id'],
			description = form.description.data,
			created_at = datetime.datetime.now(),
			updated_at = datetime.datetime.now(),
			due_date = None if request.form['due_date'] == '' else 
				datetime.datetime.strptime(request.form['due_date'], '%Y-%m-%d'),
			inceputH = form.inceputH.data,
			inceputM = form.inceputM.data,
			finalM = form.finalM.data,
			finalH = form.finalH.data,
			biliard = form.biliard.data,
			bowling = form.bowling.data,
			darts = form.darts.data,
			persons_nr = form.persons_nr.data
			)
		db.session.add(task)
		db.session.commit()
		flash('Rezervare efectuata')

		user = User.query.filter_by(id=session['user_id']).first_or_404()	
		biliardInitial = user.nrBiliard
		user.nrBiliard = int(biliardInitial or 0) + form.biliard.data
		bowlingInitial = user.nrBowling
		user.nrBowling = int(bowlingInitial or 0) + form.bowling.data
		dartsIntial = user.nrDarts
		user.nrDarts = int(dartsIntial or 0) + form.darts.data
		nrPuncteInitiale = user.nrPuncte
		user.nrPuncte = int(nrPuncteInitiale or 0) + form.biliard.data + form.bowling.data + form.darts.data
		
		minuteBiliardInitial = user.minuteBiliard
		user.minuteBiliard = int(minuteBiliardInitial or 0) + form.biliard.data * ((form.finalH.data*60 + form.finalM.data ) - ( form.inceputH.data*60 + form.inceputM.data ))
		minuteBowlingInitial = user.minuteBowling
		user.minuteBowling = int(minuteBowlingInitial or 0) + form.bowling.data * ((form.finalH.data*60 + form.finalM.data ) - ( form.inceputH.data*60 + form.inceputM.data ))
		minuteDartsInitial = user.minuteDarts
		user.minuteDarts = int(minuteDartsInitial or 0) + form.darts.data * ((form.finalH.data*60 + form.finalM.data ) - ( form.inceputH.data*60 + form.inceputM.data ))
		minuteTotalInitial = user.minuteTotal
		user.minuteTotal = int(minuteTotalInitial or 0) + (form.finalH.data*60 + form.finalM.data ) - ( form.inceputH.data*60 + form.inceputM.data )
		db.session.add(user)
		db.session.commit()

		if session['is_admin']!="True":
			return redirect(url_for('sessiontasks'))
		return redirect(url_for('tasks'))	

	users = User.query.all()
	return render_template('task/task.html', form=form, users=users, labels=labels, action='new')

# =========================================================================
#==============================EDIT TASK===================================
# =========================================================================

@app.route('/task/edit/<int:task_id>', methods=('GET', 'POST'))
@login_required
def editTask(task_id):
	task = Task.query.filter_by(id=task_id).first_or_404()
	form = TaskForm or CommentForm
	if "submitSave":
		form = TaskForm(obs=task)
		if form.validate_on_submit():
			form.populate_obj(task)
			task.title = form.title.data
			task.description = None if form.description.data is None else form.description.data
			task.updated_at = datetime.datetime.now()
			task.due_date = None if request.form['due_date'] == '' else datetime.datetime.strptime(request.form['due_date'], '%Y-%m-%d')
			task.inceputM = form.inceputM.data
			task.inceputH = form.inceputH.data
			task.finalM = form.finalM.data
			task.finalH = form.finalH.data
			task.biliard = form.biliard.data
			task.bowling = None if form.bowling.data is None else form.bowling.data
			task.darts = None if form.darts.data is None else form.darts.data
			task.persons_nr = form.persons_nr.data

			db.session.commit()
			# if session['is_admin']!="True":
			return redirect(url_for('sessiontasks'))
			# return redirect(url_for('tasks'))
			

	if "submitComment":
		form = CommentForm()
		if form.validate_on_submit():
			comment = Comment(
				task_id = task_id,
				comment_user_id = session['user_id'],
				comment_body = form.comment_body.data,
				comment_date = datetime.datetime.now()
			)
			db.session.add(comment)
			db.session.commit()
			return redirect(url_for('editTask', task_id=task.id))		

	comments = Comment.query.filter_by(task_id = task_id).order_by(Comment.date.desc())
	return render_template('task/task.html', form=form, task=task, comments=comments, action='edit')

# ==========================================================================
#==============================TASK COMMENT=================================
# ==========================================================================

@app.route('/task/comment/<int:task_id>', methods=('GET', 'POST'))
@login_required
def commentTask(task_id):
	task = Task.query.filter_by(id=task_id).first_or_404()
	form = CommentForm()
	if form.validate_on_submit():
		comment = Comment(
			task_id = task_id,
			comment_user_id = session['user_id'],
			comment_body = form.comment_body.data,
			comment_date = datetime.datetime.now()
		)
		db.session.add(comment)
		db.session.commit()
		return redirect(url_for('editTask', task_id=task.id))

	assigned_users = User.query.all()
	labels = Label.query.all()
	comments = Comment.query.all()
	return render_template('task/task.html', form=form, task=task, assigned_users=assigned_users, labels=labels, comments=comments, action='comment')

@app.route('/task/comment/edit/<int:comment_id>', methods=('GET', 'POST'))
@login_required
def editCommentTask(comment_id):
	comment = Comment.query.filter_by(id=comment_id).first_or_404()
	task = Task.query.filter_by(id=comment.task_id).first_or_404()	
	form = CommentForm(obs=comment)
	print(f'Comment: {form.comment_body}')
	if form.validate_on_submit():
		comment.body = form.comment_body.data
		db.session.commit()
	else:
		print('Form validation failed: ' + str(form.errors))
	return redirect(url_for('editTask', task_id=task.id))

# =========================================================================
#==============================DELETE TASK/COMMENT=========================
# =========================================================================

@app.route('/task/delete/<int:task_id>')
@login_required
def deleteTask(task_id):
	task = Task.query.filter_by(id=task_id).first_or_404()
	comments = Comment.query.filter_by(task_id = task_id)
	for comment in comments:
		db.session.delete(comment)
		db.session.commit()
	db.session.delete(task)
	db.session.commit()
	flash("Task deleted")
	return redirect('/tasks')

@app.route('/task/edit/deleteComment/<int:task_id>/<int:comment_id>')
@login_required
def deleteComment(task_id, comment_id):
	comment = Comment.query.filter_by(id = comment_id).first_or_404()
	db.session.delete(comment)
	db.session.commit()
	return redirect(url_for('editTask', task_id=task_id))

# =========================================================================
#==============================CLOSE/OPEN TASK=============================
# =========================================================================

@app.route('/closed/<int:task_id>')
def closed(task_id):
	task = Task.query.filter_by(id=task_id).first_or_404()
	task.is_closed = 1
	db.session.commit()
	return redirect(url_for('tasks'))
	return render_template('task/tasks.html', tasks=tasks)

@app.route('/open/<int:task_id>')
def open(task_id):
	task = Task.query.filter_by(id=task_id).first_or_404()
	task.is_closed = 0
	db.session.commit()
	return redirect(url_for('tasks'))
	return render_template('task/tasks.html', tasks=tasks)

@app.route('/biliard/<int:task_id>')
def biliard(task_id):
	task = Task.query.filter(id=task_id).first_or_404()
	task.biliard != 0 
	db.session.commit()
	return redirect(url_for('tasks'))
	return render_template('task/tasks.html', tasks=tasks)

@app.route('/bowling/<int:task_id>')
def bowling(task_id):
	task = Task.query.filter(id=task_id).first_or_404()
	task.bowling != 0 
	db.session.commit()
	return redirect(url_for('tasks'))
	return render_template('task/tasks.html', tasks=tasks)

@app.route('/darts/<int:task_id>')
def darts(task_id):
	task = Task.query.filter(id=task_id).first_or_404()
	task.darts != 0 
	db.session.commit()
	return redirect(url_for('tasks'))
	return render_template('task/tasks.html', tasks=tasks)

# =========================================================================
#==============================LABELS LIST=================================
# =========================================================================

@app.route('/labels')
@login_required
def labels():
	labels = Label.query.all()
	if not labels:
		return redirect(url_for('label'))
	else:
		return render_template('task/labels.html', labels=labels)

# =========================================================================
#==============================LABEL=======================================
# =========================================================================

@app.route('/label', methods=('GET', 'POST'))
@login_required
def label():
	form = LabelForm()
	if form.validate_on_submit():
		label = Label(
			form.name.data,
			form.color.data
			)
		db.session.add(label)
		db.session.commit()
		flash('Label created')
		return redirect(url_for('labels'))
	return render_template('task/label.html', form=form, action='new')

# =========================================================================
#==============================EDIT LABEL==================================
# =========================================================================

@app.route('/label/edit/<int:label_id>', methods=('GET', 'POST'))
@login_required
def editlabel(label_id):
	label = Label.query.filter_by(id=label_id).first_or_404()
	form = LabelForm(obs=label)
	if form.validate_on_submit():
		form.populate_obj(label)
		label.name = form.name.data
		label.color = form.color.data
		label.updated_at = datetime.datetime.now()
		db.session.commit()
		flash('Label edited')
		return redirect(url_for('labels'))
	return render_template('task/label.html', form=form, label=label, action='edit')

# =========================================================================
#==============================DELETE LABEL================================
# =========================================================================

@app.route('/label/delete/<int:label_id>')
@login_required
def deletelabel(label_id):
	label = Label.query.filter_by(id=label_id).first_or_404()
	db.session.delete(label)
	db.session.commit()
	flash('Label deleted')
	return redirect('/labels')

# =========================================================================
