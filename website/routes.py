from flask import render_template, url_for, flash, redirect, request, abort
from website import app, db
from website.models import Paczka, Kurier, Dostarczenia
from website.forms import *

@app.route("/")
@app.route("/home")
def home():
    print(Kurier.query.all())
    paczki = Paczka.query.all()
    return render_template('home.html', paczki=paczki)


@app.route("/paczka/new", methods=['GET', 'POST'])
def new_post():
    form = PaczkaForm()

    if request.method == 'POST':
        paczka = Paczka(nazwa=form.nazwa.data)
        db.session.add(paczka)
        db.session.commit()
        flash('Dodano paczkę!', 'success')

        return redirect(url_for('home'))
    return render_template('create_paczka.html', title='Nowa paczka', form=form, legend='Dodaj Paczkę')


@app.route("/kurier/new", methods=['GET', 'POST'])
def new_kurier():
    form = KurierForm()

    if request.method == 'POST':
        kurier = Kurier(nazwa=form.nazwa.data)
        db.session.add(kurier)
        db.session.commit()
        flash('Dodano kuriera!', 'success')

        return redirect(url_for('home'))
    return render_template('create_kurier.html', title='Nowy kurier', form=form, legend='Dodaj Kuriera')


@app.route("/kurier/assign", methods=['GET', 'POST'])
def assign_kurier():
    form = TerminalForm()

    # if request.method == 'POST':
    #     kurier = Kurier(nazwa=form.nazwa.data)
    #     db.session.add(kurier)
    #     db.session.commit()
    #     flash('Dodano kuriera!', 'success')

        # return redirect(url_for('home'))
    return render_template('assign_kurier.html', title='Nowy kurier', form=form, legend='Przypisz kuriera do Terminala')
