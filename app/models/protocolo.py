from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so
import app.models as models
from datetime import datetime


class Protocolo(db.Model):
    __tablename__ = "protocolos"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    numero: so.Mapped[str] = so.mapped_column(sa.String(20), unique=True, nullable=True)
    titulo: so.Mapped[str] = so.mapped_column(sa.String(150), nullable=False)
    descricao: so.Mapped[str] = so.mapped_column(sa.Text, nullable=True)
    status: so.Mapped[str] = so.mapped_column(sa.String(20), default="Recebido")
    secretaria_origem_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(models.Secretaria.id), nullable=True)
    secretaria_origem: so.Mapped[models.Secretaria] = so.relationship(foreign_keys=[secretaria_origem_id], backref="protocolos_enviados")
    secretaria_destino_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(models.Secretaria.id), nullable=True)
    secretaria_destino: so.Mapped[models.Secretaria] = so.relationship(foreign_keys=[secretaria_destino_id], backref="protocolos_recebidos")
    criado_por: so.Mapped[int] = so.mapped_column(sa.ForeignKey(models.Usuario.id))
    usuario: so.Mapped[models.Usuario] = so.relationship()
    arquivo: so.Mapped[str] = so.mapped_column(sa.String(200), nullable=True)
    data_criacao: so.Mapped[datetime] = so.mapped_column(sa.DateTime, default=datetime.now)
    data_atualizacao: so.Mapped[datetime] = so.mapped_column(sa.DateTime, default=datetime.now, onupdate=datetime.now)
    historico: so.Mapped[list["Tramitacao"]] = so.relationship(back_populates="protocolo", cascade="all, delete-orphan", order_by="Tramitacao.data.desc()")



    def atribuir_numero_por_id(self):
        ano = datetime.now().year
        seq = str(self.id).zfill(5)
        self.numero = f"{ano}-{seq}"
