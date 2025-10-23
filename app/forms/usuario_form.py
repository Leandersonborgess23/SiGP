from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from app.controllers.usuarioController import UsuarioController
from wtforms import ValidationError
from flask import request
from app.models.usuario import Usuario


class UsuarioForm(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Salvar')

    def validate_username(self, field):
        usuario_existente = Usuario.query.filter_by(username=field.data.strip()).first()
        if not UsuarioController.checar_unicidade(field.data.strip(), 'username'):
            raise ValidationError('Nome de usuário já cadastrado.')

    def validate_email(self, field):
        usuario_existente = Usuario.query.filter_by(email=field.data.strip().lower()).first()
        if not UsuarioController.checar_unicidade(field.data.strip().lower(), 'email'):
            raise ValidationError('Email já cadastrado.')
