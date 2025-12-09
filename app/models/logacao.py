from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import datetime
from flask_login import current_user

class LogAcao(db.Model):
    __tablename__ = "logs_acoes"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    usuario_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("usuarios.id"), nullable=True)
    usuario = so.relationship("Usuario")
    acao: so.Mapped[str] = so.mapped_column(sa.String(100), nullable=False)
    entidade: so.Mapped[str] = so.mapped_column(sa.String(100), nullable=False)
    entidade_id: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    detalhe: so.Mapped[str] = so.mapped_column(sa.Text, nullable=True)
    data: so.Mapped[datetime] = so.mapped_column(sa.DateTime, default=datetime.utcnow)
