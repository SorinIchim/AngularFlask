#Set the path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy

from __init__ import app, db

#models
from models.comment import *
from models.label import *
from models.task import *
from models.user import *

class UserTest(unittest.TestCase):
	def setUp(self):
		db_username = app.config['DB_USERNAME']
		db_password = app.config['DB_PASSWORD']
		db_host = app.config['DB_HOST']
		self.db_uri = "mysql+pymysql://%s:%s@%s/" % (db_username, db_password, db_host)
		app.config['TESTING']=True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['TASK_DATABASE_NAME'] = 'test_task'
		app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri + app.config['TASK_DATABASE_NAME']
		engine = sqlalchemy.create_engine(self.db_uri)
		conn = engine.connect()
		conn.execute("commit")
		conn.execute("CREATE DATABASE " + app.config['TASK_DATABASE_NAME'])
		db.create_all()
		conn.close()
		self.app = app.test_client()
	
	def tearDown(self):
		db.session.remove()
		engine = sqlalchemy.create_engine(self.db_uri)
		conn = engine.connect()
		conn.execute("commit")
		conn.execute("DROP DATABASE " + app.config['TASK_DATABASE_NAME'])
		conn.close()

# =================================================================================================
# ==========================================TEST REGISTER==========================================
# =================================================================================================

	def register(self):
		return self.app.post('/register', data=dict(
			fullname = "Test register",
			email = "test@test.com",
			username = "test",
			password = "Parola123",
			confirm = "Parola123"
			),
		follow_redirects = True)
		
	def test_register(self):
		rv = self.register()
		assert 'User created' in str(rv.data)

# =================================================================================================
# ========================================TEST LOGIN/LOGOUT========================================
# =================================================================================================

	def login(self, username, password):
		return self.app.post('/login', data=dict(
			username = username,
			password = password
			),
		follow_redirects=True)

	def logout(self):
		return self.app.get('/logout', follow_redirects=True)

	def test_login_fail(self):
		rv = self.login("Sorin", "Parola123")
		assert "Incorrect username and password" in str(rv.data)

	def test_login_logout(self):
		self.register()
		rv = self.login('test', 'Parola123')
		assert "User test logged in" in str(rv.data)
		rv = self.logout()
		assert 'User logged out' in str(rv.data)

# =================================================================================================
# ===========================================TEST LABEL============================================
# =================================================================================================

	# def create_label(self, name='test', color='blue'):
	# 	return self.app.post('/label', data=dict(
	# 		name = name,
	# 		color = color),
	# 	follow_redirects=True)

	# def test_create_label(self):
	# 	rv = self.create_label()
	# 	assert 'Label created' in str(rv.data)

# =================================================================================================
# ========================================TEST EDIT LABEL==========================================
# =================================================================================================

	# def edit_label(self, id, name, color):
	# 	return self.app.post(f'/label/edit/{id}', data=dict(
	# 		name = name,
	# 		color = color),
	# 	follow_redirects=True)

	# def test_edit_label(self):
	# 	self.create_label('test', 'blue')
	# 	rv = self.edit_label(1, 'Test', 'red')
	# 	assert 'Label edited' in str(rv.data)

# =================================================================================================
# =======================================TEST DELETE LABEL=========================================
# =================================================================================================

	# def delete_label(self, id=1):
	# 	return self.app.post(f'/label/delete/{id}', follow_redirects=True)

	# def test_delete_label(self):
	# 	self.create_label()
	# 	rv = self.delete_label()
	# 	assert 'Label deleted' in str(rv.data)

if __name__=='__main__':
	unittest.main()
	