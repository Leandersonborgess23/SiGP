from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FileField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class ProtocoloForm(FlaskForm):
    titulo = StringField("Título", validators=[DataRequired(), Length(max=150)])
    descricao = TextAreaField("Descrição", validators=[Optional()])
    secretaria_destino_id = SelectField("Secretaria Destino", coerce=int, validators=[Optional()])
    arquivo = FileField("Anexar PDF (opcional)")
    submit = SubmitField("Salvar Protocolo")
