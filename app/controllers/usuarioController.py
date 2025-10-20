from app import db
from app.models.usuario import Usuario
from werkzeug.security import generate_password_hash
import sqlalchemy as sa

class UsuarioController:

    @staticmethod
    def salvar(form):
        try:
            usuario = Usuario()
            form.populate_obj(usuario)
            usuario.password_hash = generate_password_hash(form.password.data)
            db.session.add(usuario)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print("Erro ao salvar usuário:", e)
            return False

    @staticmethod
    def checar_unicidade(campo, tipo):
        if tipo == 'username':
            if Usuario.query.filter_by(username=campo).first():
                return False
        if tipo == 'email':
            if Usuario.query.filter_by(email=campo).first():
                return False
        return True

    @staticmethod
    def listar_usuarios():
        return Usuario.query.all()

    @staticmethod
    def buscar_por_username(username):
        return Usuario.query.filter_by(username=username).first()
    
    @staticmethod
    def atualizar_usuario(id, form):
        usuario = db.session.get(Usuario, id)
        if usuario:
            form.populate_obj(usuario)  # Preenche o objeto com os dados do form
            db.session.commit()
            print('Usuário atualizado com sucesso!')
            return True
        else:
            print('Usuário não encontrado.')
            return False

    @staticmethod
    def remover_usuario(id):
        usuario = db.session.get(Usuario, id)
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
            print('Usuário removido com sucesso!')
            return True
        else:
            print('Usuário não encontrado.')
            return False