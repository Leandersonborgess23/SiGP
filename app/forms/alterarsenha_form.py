from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length

class AlterarSenhaForm(FlaskForm):
    senha_atual = PasswordField( "Senha atual", validators=[DataRequired(message="Informe sua senha atual.")] )
    nova_senha = PasswordField("Nova Senha", validators=[DataRequired(), Length(min=6, message="A senha deve ter pelo menos 6 caracteres.")])
    confirmar_senha = PasswordField("Confirmar Senha", validators=[DataRequired(), EqualTo("nova_senha", message="As senhas não conferem.")])
    submit = SubmitField("Atualizar Senha")
