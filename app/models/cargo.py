from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so
import app.models as models

class Cargo(db.Model):
    __tablename__ = "cargos"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    nome: so.Mapped[str] = so.mapped_column(sa.String(120), nullable=False)
    descricao: so.Mapped[str] = so.mapped_column(sa.Text)
    servidores: so.Mapped[list] = so.relationship("Servidor", back_populates="cargo")
