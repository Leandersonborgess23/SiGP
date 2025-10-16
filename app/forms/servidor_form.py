from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class ServidorForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    cpf = StringField('CPF')
    email = StringField('Email')
    telefone = StringField('Telefone')
    cargo_id = SelectField('Cargo', coerce=int, choices=[])
    secretaria_id = SelectField('Secretaria', coerce=int, choices=[])
    submit = SubmitField('Salvar')
