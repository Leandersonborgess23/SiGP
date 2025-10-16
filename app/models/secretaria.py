from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so
import app.models as models

class Secretaria(db.Model):
    __tablename__ = "secretarias"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    nome: so.Mapped[str] = so.mapped_column(sa.String(120), nullable=False)
    descricao: so.Mapped[str] = so.mapped_column(sa.Text)
    prefeitura_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(models.Prefeitura.id), index=True)
    servidores: so.Mapped[list] = so.relationship("Servidor", back_populates="secretaria")
    prefeitura: so.Mapped[models.Prefeitura] = so.relationship(back_populates="secretarias")
