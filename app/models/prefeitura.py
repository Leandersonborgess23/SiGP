from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so

class Prefeitura(db.Model):
    __tablename__ = "prefeitura"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    nome: so.Mapped[str] = so.mapped_column(sa.String(200), nullable=False)
    cnpj: so.Mapped[str] = so.mapped_column(sa.String(20), unique=True)
    endereco: so.Mapped[str] = so.mapped_column(sa.String(255))
    telefone: so.Mapped[str] = so.mapped_column(sa.String(30))
    email: so.Mapped[str] = so.mapped_column(sa.String(120))
    secretarias: so.Mapped[list] = so.relationship("Secretaria", back_populates="prefeitura")
