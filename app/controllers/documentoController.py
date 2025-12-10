import os
from flask import current_app
from werkzeug.utils import secure_filename
from datetime import datetime

from app import db
from app.models.documento import Documento


class DocumentoController:

    @staticmethod
    def listar_documentos():
        return Documento.query.filter_by(ativo=True).order_by(Documento.data_criacao.desc()).all()

    @staticmethod
    def buscar_por_id(id):
        return Documento.query.get(id)

    @staticmethod
    def criar_documento(form, usuario_id):
        """Cria um documento e salva o arquivo"""
        arquivo = form.arquivo.data

        if arquivo:
            nome_seguro = secure_filename(arquivo.filename)
            caminho = os.path.join(current_app.config["UPLOAD_DOCUMENTOS"], nome_seguro)
            arquivo.save(caminho)
        else:
            nome_seguro = None

        documento = Documento(
            titulo=form.titulo.data,
            descricao=form.descricao.data,
            categoria=form.categoria.data,
            arquivo=nome_seguro,
            criado_por=usuario_id,
            secretaria_id=form.secretaria_id.data,
            privado=form.privado.data,
            tags=form.tags.data
        )

        db.session.add(documento)
        db.session.commit()
        return documento

    @staticmethod
    def atualizar_documento(documento, form):
        """Atualiza documento e faz upload se necessário"""
        documento.titulo = form.titulo.data
        documento.descricao = form.descricao.data
        documento.categoria = form.categoria.data
        documento.secretaria_id = form.secretaria_id.data
        documento.privado = form.privado.data
        documento.tags = form.tags.data

        arquivo = form.arquivo.data
        if arquivo:
            nome_seguro = secure_filename(arquivo.filename)
            caminho = os.path.join(current_app.config["UPLOAD_DOCUMENTOS"], nome_seguro)
            arquivo.save(caminho)
            documento.arquivo = nome_seguro

        db.session.commit()
        return documento

    @staticmethod
    def deletar_documento(documento):
        if documento.arquivo:
            caminho_arquivo = os.path.join(
                current_app.config["UPLOAD_DOCUMENTOS"], documento.arquivo
            )

            if os.path.exists(caminho_arquivo):
                os.remove(caminho_arquivo)

        db.session.delete(documento)
        db.session.commit()
        return True