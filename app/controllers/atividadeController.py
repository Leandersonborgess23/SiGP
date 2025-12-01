from app.models import Atividade

class AtividadeController:

    @staticmethod
    def listar(limit=None):
        query = Atividade.query.order_by(Atividade.data.desc())
        if limit:
            query = query.limit(limit)
        return query.all()

    @staticmethod
    def listar_todas():
        return Atividade.query.order_by(Atividade.data.desc()).all()
