from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so
import app.models as models
from datetime import datetime

class Evento(db.Model):
    __tablename__ = "eventos"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    titulo: so.Mapped[str] = so.mapped_column(sa.String(150), nullable=False)
    descricao: so.Mapped[str] = so.mapped_column(sa.Text)
    data_inicio: so.Mapped[datetime] = so.mapped_column(sa.DateTime, nullable=False)
    data_fim: so.Mapped[datetime] = so.mapped_column(sa.DateTime, nullable=True)

    criado_por: so.Mapped[int] = so.mapped_column(sa.ForeignKey(models.Usuario.id))
    usuario: so.Mapped[models.Usuario] = so.relationship(back_populates="eventos")
