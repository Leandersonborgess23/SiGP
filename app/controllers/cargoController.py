from app import db
from app.models.cargo import Cargo

class CargoController:

    @staticmethod
    def criar(form):
        try:
            cargo = Cargo()
            form.populate_obj(cargo)
            db.session.add(cargo)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print("Erro ao cadastrar cargo:", e)
            return False

    @staticmethod
    def listar():
        return Cargo.query.all()

    @staticmethod
    def remover(id):
        cargo = Cargo.query.get(id)
        if cargo:
            db.session.delete(cargo)
            db.session.commit()
            return True
        return False
