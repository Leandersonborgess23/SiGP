from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Permanecer conectado')
    submit = SubmitField('Entrar')

    def validate_username(self, field):
        if field.data.lower() == 'admin':
            raise ValidationError('O nome "admin" está reservado. Escolha outro.')