from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class CargoForm(FlaskForm):
    nome = StringField("Nome do Cargo", validators=[DataRequired(), Length(max=120)])
    descricao = TextAreaField("Descrição", validators=[Length(max=255)])
    submit = SubmitField("Cadastrar")
