from app import db
from app.models.atividade import Atividade
from flask_login import current_user

def registrar_atividade(acao):
    try:
        usuario = current_user.username if current_user.is_authenticated else "Sistema"
        registro = Atividade(usuario=usuario, acao=acao)
        db.session.add(registro)
        db.session.commit()
    except:
        pass  # evita crash caso algo falhe
