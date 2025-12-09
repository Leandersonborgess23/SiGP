from app import db
from app.models.logacao import LogAcao
from flask_login import current_user

def registrar_log(acao, entidade, entidade_id=None, detalhe=None):
    try:
        log = LogAcao(
            usuario_id=current_user.id if current_user.is_authenticated else None,
            acao=acao,
            entidade=entidade,
            entidade_id=entidade_id,
            detalhe=detalhe
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("Erro ao registrar log:", e)
