import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import render_template, redirect, url_for, request
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server
from __init__ import app, db
from models import *
from models.tarife import Produs
from tarife.form import ProdusForm

from flask_cors import CORS;
from flask import Flask, jsonify;
from flask_mysqldb import MySQL
import json

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

manager.add_command("runserver", Server(
	use_debugger = True,
	use_reloader = True,
	host = os.getenv('IP', '127.0.0.1'),
	port = int(os.getenv('PORT', 5000))
	)
)

# ===========================================================================
# app = Flask(__name__)
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'sorin'
app.config['MYSQL_PASSWORD'] = 'Parola123'
app.config['MYSQL_DB'] = 'test'
mysql = MySQL(app)
CORS(app)


@app.route("/", methods=['GET'])
def index():
    return "Welcome to CodezUp";


@app.route("/listaProduse/", methods = ['GET', 'POST'])
def ListaProduse():
    # if "add":
    #     form = ProdusForm()
    #     if "form.name.data != null":
    #         produs = Produs(
    #             name = form.name.data,
    #             price = form.price.data,
    #             stock = form.stock.data
    #         )
    #     print("=======commit========")
    #     db.session.add(produs)
    #     db.session.commit()

    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM produs''')
    row_headers=[x[0] for x in cursor.description] #this will extract row headers <<< MOMENTAN NU MERGE
    rv = cursor.fetchall()
    Produse=[]
    for result in rv:
        Produse.append(dict(zip(row_headers,result)))
    return jsonify(Produse)

# V1 ===================
# def ListaProduse(produs):
#     produsAdd = Produs(
#         name = produs.name,
#         price = produs.price,
#         stock = produs.stock
#     )
#     db.session.add(produsAdd)
#     db.session.commit()
#     return redirect(url_for('ListaProduse'))

# v2==========
    # if "addProdusButton":
    #     name = produs.name,
    #     price = produs.price,
    #     stock = produs.stock
    #     print(name)

# ==========================================================================================
# ====================================== DELETE ROUTE ======================================
# ==========================================================================================

# @app.route('/listaProduse/delete/<int:produs_id>')
# def deleteProdus(produs_id):
    # VARIANTA 1
    # cursor = mysql.connection.cursor()
    # cursor.execute('''SELECT * FROM produs WHERE produs.id="produs_id"''')
    # rv = cursor.fetchone()

    # VARIANTA 2
    # LINK: https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html
    # cursor = mysql.connection.cursor()
    # select_stmt = "SELECT * FROM produs WHERE produs.id= %(produs_id)s"
    # cursor.execute(select_stmt, {'produs_id': 1})
    # rv = cursor.fetchone()

    # VARIANTA 3
    # rv = Produs.query.filter(Produs.id == produs_id).first()

    # db.session.delete(rv)
    # db.session.commit()
    # return redirect(url_for('ListaProduse'))

@app.route('/listaProduse/delete/<int:produs_id>')
def deleteProdus(produs_id):
    produs1 = Produs.query.filter(Produs.id==produs_id).first_or_404()
    db.session.delete(produs1)
    db.session.commit()
    return redirect(url_for('ListaProduse'))

# ==========================================================================================
# ====================================== UPDATE ROUTE ======================================
# ==========================================================================================

@app.route('/listaProduse/update/<int:produs_id>')
def updateProdus(produs_id):
    produs1 = Produs.query.filter(Produs.id==produs_id).first_or_404()

    form = ProdusForm()
    if "form.name.data != null":
        produs = Produs(
            name = form.name.data,
            price = form.price.data,
            stock = form.stock.data
        )
    print("=======commit========")
    db.session.add(produs)
    db.session.commit()
    return redirect(url_for('ListaProduse'))

# ==========================================================================================
# ======================================              ======================================
# ==========================================================================================

if __name__ == '__main__':
    app.run(debug=True)

	