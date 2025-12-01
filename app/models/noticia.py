from app import db
from datetime import datetime

class Noticia(db.Model):
    __tablename__ = "noticias"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    data_publicacao = db.Column(db.DateTime, default=datetime.utcnow)
    imagem = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"<Notícia {self.titulo}>"
