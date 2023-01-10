from flask import render_template, url_for, flash, redirect, request, abort
from website import app, db, bcrypt
from website.models import Kurier
from website.forms import RegistrationForm, LoginForm, ExchangeForm, PostForm
from flask_login import login_user, current_user, logout_user, login_required
from website import prices

# forms pozwalają na sprawdzenie podawanych przez użytkownika danych


@app.route("/")
@app.route("/home")
def home():

    print(Kurier.query.all())
    return render_template(
        "home.html"
    )  # dzięki temu będziemy mieć dostęp do postów w pliku html
