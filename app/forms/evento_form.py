from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeLocalField, SubmitField
from wtforms.validators import DataRequired

class EventoForm(FlaskForm):
    titulo = StringField("Título", validators=[DataRequired()])
    descricao = TextAreaField("Descrição")
    data_inicio = DateTimeLocalField("Início", format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    data_fim = DateTimeLocalField("Fim", format='%Y-%m-%dT%H:%M')
    submit = SubmitField("Salvar")
