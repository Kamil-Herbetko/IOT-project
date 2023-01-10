from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import datetime
#from models import Administrator

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site4.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


from website.models import *
db.create_all()




from website import routes

