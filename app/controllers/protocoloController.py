import os
from werkzeug.utils import secure_filename
from app import db
from flask import current_app
from app.models.protocolo import Protocolo
from app.models.tramitacao import Tramitacao
from app.models.prefeitura import Prefeitura
from app.utils.logger import registrar_log
from datetime import datetime
from flask_login import current_user


ALLOWED_EXT = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

class ProtocoloController:

    @staticmethod
    def criar(form):
        try:
            p = Protocolo(
                titulo=form.titulo.data.strip(),
                descricao=form.descricao.data.strip() if form.descricao.data else None,
                secretaria_origem_id=None,  
                secretaria_destino_id=form.secretaria_destino_id.data if form.secretaria_destino_id.data else None,
                criado_por=current_user.id if current_user and hasattr(current_user, 'id') else None
            )

            arquivo_filename = None
            if form.arquivo.data:
                file = form.arquivo.data
                if file.filename and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    caminho = os.path.join(current_app.static_folder, "uploads", "protocolos")
                    os.makedirs(caminho, exist_ok=True)
                    file.save(os.path.join(caminho, filename))
                    arquivo_filename = f"uploads/protocolos/{filename}"
                    p.arquivo = arquivo_filename

            try:
                if hasattr(current_user, "servidor") and current_user.servidor and current_user.servidor.secretaria:
                    p.secretaria_origem_id = current_user.servidor.secretaria.id
            except Exception:
                pass

            db.session.add(p)
            db.session.commit()

            p.gerar_numero()
            db.session.commit()

            t = Tramitacao(
                protocolo_id=p.id,
                de_secretaria_id=None,
                para_secretaria_id=p.secretaria_destino_id,
                observacao="Protocolo registrado",
                usuario_id=current_user.id if current_user and hasattr(current_user, 'id') else None
            )
            db.session.add(t)
            db.session.commit()
            
            registrar_log(
                acao="Criou Protocolo",
                entidade="Protocolo",
                entidade_id=p.id,
                detalhe=f"Título: {p.titulo}"
            )

            return True
        except Exception as e:
            db.session.rollback()
            print("Erro ao criar protocolo:", e)
            return False

    @staticmethod
    def listar(filtros=None):
        q = Protocolo.query.order_by(Protocolo.data_criacao.desc())
        if filtros:
            if filtros.get("numero"):
                q = q.filter(Protocolo.numero == filtros["numero"])
            if filtros.get("status"):
                q = q.filter(Protocolo.status == filtros["status"])
            if filtros.get("secretaria_id"):
                q = q.filter(
                    (Protocolo.secretaria_origem_id == filtros["secretaria_id"]) |
                    (Protocolo.secretaria_destino_id == filtros["secretaria_id"])
                )
        return q.all()

    @staticmethod
    def buscar(id):
        return Protocolo.query.get(id)

    @staticmethod
    def remover(id):
        p = Protocolo.query.get(id)
        if p:
            try:
                db.session.delete(p)
                db.session.commit()

                registrar_log(
                    acao="Removeu Protocolo",
                    entidade="Protocolo",
                    entidade_id=id
                )

                return True
            except Exception as e:
                db.session.rollback()
                print("Erro ao remover protocolo:", e)
        return False

    @staticmethod
    def tramitar(protocolo_id, form):
        try:
            p = Protocolo.query.get(protocolo_id)
            if not p:
                return False

            t = Tramitacao(
                protocolo_id=p.id,
                de_secretaria_id=p.secretaria_destino_id or p.secretaria_origem_id,
                para_secretaria_id=form.para_secretaria_id.data,
                observacao=form.observacao.data.strip() if form.observacao.data else None,
                usuario_id=current_user.id if current_user and hasattr(current_user, 'id') else None
            )

            if form.arquivo.data:
                file = form.arquivo.data
                if file.filename and allowed_file(file.filename):

                    filename = secure_filename(file.filename)
                    caminho = os.path.join(current_app.static_folder, "uploads", "tramitacoes")
                    os.makedirs(caminho, exist_ok=True)

                    file.save(os.path.join(caminho, filename))

                    t.arquivo = f"uploads/tramitacoes/{filename}"

                    registrar_log(
                        acao="Anexou arquivo em tramitação",
                        entidade="Tramitacao",
                        entidade_id=t.id,
                        detalhe=f"Arquivo: {filename}"
                    )
                    
            p.secretaria_destino_id = form.para_secretaria_id.data
            p.status = "Em Análise"
            p.data_atualizacao = datetime.utcnow()

            db.session.add(t)
            db.session.commit()

            registrar_log(
                acao="Tramitou Protocolo",
                entidade="Protocolo",
                entidade_id=protocolo_id,
                detalhe=f"Novo destino: {form.para_secretaria_id.data}"
            )

            if t.arquivo:
                registrar_log(
                    acao="Anexou Arquivo na Tramitação",
                    entidade="Tramitacao",
                    entidade_id=t.id,
                    detalhe=f"Arquivo: {t.arquivo}"
                )

            return True
        except Exception as e:
            db.session.rollback()
            print("Erro ao tramitar protocolo:", e)
            return False