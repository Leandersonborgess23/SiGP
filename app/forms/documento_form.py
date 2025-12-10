from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, FileField
from wtforms.validators import DataRequired, Length
from app.models.secretaria import Secretaria


class DocumentoForm(FlaskForm):
    titulo = StringField("Título", validators=[DataRequired(), Length(max=200)])
    descricao = TextAreaField("Descrição")
    categoria = StringField("Categoria", validators=[DataRequired(), Length(max=100)])

    arquivo = FileField("Arquivo (PDF, DOCX, JPG, PNG)")

    secretaria_id = SelectField("Secretaria", coerce=int)
    privado = BooleanField("Documento Restrito")
    tags = StringField("Tags (separar por vírgula)")

    def carregar_secretarias(self):
        self.secretaria_id.choices = [
            (0, "Nenhuma")
        ] + [(s.id, s.nome) for s in Secretaria.query.all()]
