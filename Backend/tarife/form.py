from flask_wtf import Form
from wtforms import validators, StringField, PasswordField, TextAreaField, DateTimeField, DecimalField, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField

class ProdusForm(Form):
	name = StringField('name', [validators.Required()])
	price = DecimalField('price')
	stock = DecimalField('stock')
