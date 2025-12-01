from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, Optional

class PerfilForm(FlaskForm):
    username = StringField("Nome de usuário", validators=[DataRequired()])
    email = StringField("E-mail", validators=[Email()])
    foto = FileField("Foto de perfil (opcional)")
    submit = SubmitField("Salvar alterações")
