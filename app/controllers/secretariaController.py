from app import db
from app.models.secretaria import Secretaria

class SecretariaController:

    @staticmethod
    def criar(form):
        try:
            sec = Secretaria()
            form.populate_obj(sec)
            db.session.add(sec)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print("Erro criar secretaria:", e)
            return False

    @staticmethod
    def listar():
        return Secretaria.query.all()
