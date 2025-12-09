from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so
import app.models as models
from datetime import datetime
from sqlalchemy.orm import backref


class Tramitacao(db.Model):
    __tablename__ = "tramitacoes"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    protocolo_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(models.Protocolo.id), nullable=False)
    protocolo: so.Mapped[models.Protocolo] = so.relationship(back_populates="historico")
    de_secretaria_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(models.Secretaria.id), nullable=True)
    de_secretaria: so.Mapped[models.Secretaria] = so.relationship(foreign_keys=[de_secretaria_id])
    para_secretaria_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(models.Secretaria.id), nullable=True)
    para_secretaria: so.Mapped[models.Secretaria] = so.relationship(foreign_keys=[para_secretaria_id])
    observacao: so.Mapped[str] = so.mapped_column(sa.Text, nullable=True)
    usuario_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(models.Usuario.id))
    usuario: so.Mapped[models.Usuario] = so.relationship()
    data: so.Mapped[datetime] = so.mapped_column(sa.DateTime, default=datetime.now)
    arquivo: so.Mapped[str] = so.mapped_column(sa.String(200), nullable=True)

