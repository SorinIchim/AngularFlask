from __init__ import app
from flask import render_template, redirect, url_for, flash, session, abort, request
from tarife.form import ProdusForm
from __init__ import db
from models.tarife import Produs
from user.decorators import login_required, admin
from slugify import slugify
import os

# =========================================================================
# ==============================ADAUGA PRODUS==============================
# =========================================================================

@app.route('/tarife-bar-AV', methods=('GET', 'POST'))
@login_required
@admin
def tarifeBarAV(page=1):

	form = ProdusForm()
	if form.validate_on_submit():
		produs = Produs(
			name = form.name.data,
			price = form.price.data,
			stock = form.stock.data
		)
		db.session.add(produs)
		db.session.commit()
		return redirect(url_for('tarifeBarAV'))
	produse = Produs.query.order_by(Produs.name.asc())
	return render_template('tarife/tarife-bar-AV.html', form=form, produse=produse)

# =========================================================================
# ==============================STERGERE PRODUS============================
# =========================================================================

@app.route('/tarife-bar-AV/stergeProdus/<int:produs_id>')
@login_required
@admin
def stergeProdus(produs_id):
	produs = Produs.query.filter_by(id=produs_id).first_or_404()
	db.session.delete(produs)
	db.session.commit()
	flash('Produs sters')
	return redirect(url_for('tarifeBarAV'))


# =========================================================================
#==============================VIZUALIZARE TASK============================
# =========================================================================

@app.route('/tarife-bar')
def tarifeBar(page=1):
	produse = Produs.query.order_by(Produs.name.asc())
	return render_template('tarife/tarife-bar.html', produse=produse)
