from app import db
from app.models.evento import Evento
from flask_login import current_user

class EventoController:

    @staticmethod
    def criar(form):
        evento = Evento(
            titulo=form.titulo.data,
            descricao=form.descricao.data,
            data_inicio=form.data_inicio.data,
            data_fim=form.data_fim.data,
            criado_por=current_user.id
        )
        db.session.add(evento)
        db.session.commit()
        return True

    @staticmethod
    def listar():
        return Evento.query.order_by(Evento.data_inicio.asc()).all()

    @staticmethod
    def remover(id):
        evento = Evento.query.get(id)
        if evento:
            db.session.delete(evento)
            db.session.commit()
            return True
        return False
