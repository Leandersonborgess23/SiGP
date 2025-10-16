from app import db
from app.models.servidor import Servidor

class ServidorController:

    @staticmethod
    def criar(form):
        try:
            s = Servidor()
            form.populate_obj(s)
            db.session.add(s)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print("Erro criar servidor:", e)
            return False

    @staticmethod
    def listar():
        return Servidor.query.all()

    @staticmethod
    def buscar(id):
        return Servidor.query.get(id)

    @staticmethod
    def remover(id):
        s = Servidor.query.get(id)
        if s:
            db.session.delete(s)
            db.session.commit()
            return True
        return False
