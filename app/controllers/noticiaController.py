import os
from app import db
from app.models import Noticia
from werkzeug.utils import secure_filename
from flask import current_app

class NoticiaController:

    @staticmethod
    def criar(form):
        imagem_filename = None

        if form.imagem.data:
            filename = secure_filename(form.imagem.data.filename)
            caminho = os.path.join(current_app.static_folder, "img/noticias")
            os.makedirs(caminho, exist_ok=True)
            form.imagem.data.save(os.path.join(caminho, filename))
            imagem_filename = f"img/noticias/{filename}"

        noticia = Noticia(
            titulo=form.titulo.data,
            conteudo=form.conteudo.data,
            imagem=imagem_filename
        )

        db.session.add(noticia)
        db.session.commit()
        return True

    @staticmethod
    def listar(limit=None):
        query = Noticia.query.order_by(Noticia.data_publicacao.desc())
        return query.limit(limit).all() if limit else query.all()

    @staticmethod
    def remover(id):
        noticia = Noticia.query.get(id)
        if not noticia:
            return False
        db.session.delete(noticia)
        db.session.commit()
        return True
