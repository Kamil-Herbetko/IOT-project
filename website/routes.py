from flask import Response, render_template, url_for, flash, redirect, request, abort
from website import app, db
from website.models import Paczka, Kurier, Dostarczenia
from website.forms import *


@app.route("/")
@app.route("/home")
def home():
    paczki = Paczka.query.all()
    return render_template("home.html", paczki=paczki)

@app.route("/dostarczenia")
def dostarczenia():
    dostarczenia = Dostarczenia.query.all()
    paczki = Paczka.query
    kurierzy = Kurier.query
    return render_template("dostarczenia.html", dostarczenia=dostarczenia, paczki=paczki, kurierzy=kurierzy)


@app.route("/kuriers")
def kuriers():
    kurier_objs = Kurier.query.all()
    return render_template("kuriers.html", kuriers=kurier_objs)


@app.route("/paczka/new", methods=["GET", "POST"])
def new_post():
    form = PaczkaForm()

    if request.method == "POST":
        paczka = Paczka(nazwa=form.nazwa.data)
        db.session.add(paczka)
        db.session.commit()
        flash("Dodano paczkę!", "success")

        return redirect(url_for("home"))
    return render_template(
        "create_paczka.html", title="Nowa paczka", form=form, legend="Dodaj Paczkę"
    )


@app.route("/kurier/new", methods=["GET", "POST"])
def new_kurier():
    form = KurierForm()

    if request.method == "POST":
        kurier = Kurier(nazwa=form.nazwa.data)
        db.session.add(kurier)
        db.session.commit()
        flash("Dodano kuriera!", "success")

        return redirect(url_for("kuriers"))
    return render_template(
        "create_kurier.html", title="Nowy kurier", form=form, legend="Dodaj Kuriera"
    )


@app.route("/paczka/<paczka_id>", methods=["DELETE"])
def delete_paczka(paczka_id):
    paczka = Paczka.query.filter_by(id=paczka_id).first()
    db.session.delete(paczka)
    db.session.commit()
    flash("Usunięto paczkę!", "success")
    return Response()


@app.route("/kurier/<kurier_id>", methods=["DELETE"])
def delete_kurier(kurier_id):
    kurier = Kurier.query.filter_by(id=kurier_id).first()
    db.session.delete(kurier)
    db.session.commit()
    flash("Usunięto kuriera!", "success")
    return Response()


@app.route("/kurier/assign", methods=["GET", "POST"])
def assign_kurier():
    form = TerminalForm()

    if request.method == "POST":
        # przypisz kuriera do tego raspberry
        if form.terminal.data == "RASP1":
            # terminal1 = form.kurier.data
            pass
        elif form.terminal.data == "RASP2":
            pass

        flash("Przypisano kuriera!", "success")

        return redirect(url_for("home"))
    return render_template(
        "assign_kurier.html",
        title="Nowy kurier",
        form=form,
        legend="Przypisz kuriera do Terminala",
    )
