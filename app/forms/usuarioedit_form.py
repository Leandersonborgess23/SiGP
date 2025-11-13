from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email
from app.controllers.usuarioController import UsuarioController
from wtforms import ValidationError
from app.models.usuario import Usuario


class UsuarioEditForm(FlaskForm):
    id = IntegerField()
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Salvar Alterações')

    def validate_username(self, field):
        usuario_existente = Usuario.query.filter_by(username=field.data.strip()).first()
        if usuario_existente is not None and usuario_existente.id != self.id.data:
            if not UsuarioController.checar_unicidade(field.data.strip(), 'username'):
                raise ValidationError('Nome de usuário já cadastrado.')

    def validate_email(self, field):
        usuario_existente = Usuario.query.filter_by(email=field.data.strip().lower()).first()
        if usuario_existente is not None and usuario_existente.id != self.id.data:
            if not UsuarioController.checar_unicidade(field.data.strip().lower(), 'email'):
                raise ValidationError('Email já cadastrado.')