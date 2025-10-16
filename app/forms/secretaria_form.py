from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class SecretariaForm(FlaskForm):
    nome = StringField("Nome da Secretaria", validators=[DataRequired(), Length(max=100)])
    descricao = TextAreaField("Descrição", validators=[Length(max=255)])
    submit = SubmitField("Cadastrar")
