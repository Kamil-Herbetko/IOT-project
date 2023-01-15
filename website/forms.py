from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, DateField, SelectField
from wtforms.validators import DataRequired

class PaczkaForm(FlaskForm):
    nazwa = StringField('Nazwa', validators=[DataRequired()])
    submit = SubmitField('Dodaj paczkę')

class KurierForm(FlaskForm):
    nazwa = StringField('Nazwa', validators=[DataRequired()])
    submit = SubmitField('Dodaj kuriera')

TERMINALS = ['RASP1', 'RASP2']
class TerminalForm(FlaskForm):
    terminal = SelectField('Terminal', validators=[DataRequired()], choices=TERMINALS)  #do przemyślenia
    kurier = StringField('Kurier', validators=[DataRequired()])
    submit = SubmitField('Przypisz kuriera')