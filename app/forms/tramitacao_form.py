from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, SubmitField, FileField
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired, Optional

class TramitacaoForm(FlaskForm):
    para_secretaria_id = SelectField("Encaminhar para", coerce=int, validators=[DataRequired()])
    observacao = TextAreaField("Observação", validators=[Optional()])
    arquivo = FileField("Anexo (PDF)", validators=[FileAllowed(['pdf'], 'Apenas PDFs são permitidos')])
    submit = SubmitField("Tramitar")
