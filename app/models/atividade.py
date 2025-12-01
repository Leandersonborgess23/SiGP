from app import db
from datetime import datetime

class Atividade(db.Model):
    __tablename__ = "atividades"

    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(120))  # quem fez a ação (pode ser None)
    acao = db.Column(db.String(255), nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)
