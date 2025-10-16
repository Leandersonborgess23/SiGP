from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so
from typing import Optional

class Servidor(db.Model):
    __tablename__ = "servidores"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    nome: so.Mapped[str] = so.mapped_column(sa.String(150), nullable=False)
    cpf: so.Mapped[Optional[str]] = so.mapped_column(sa.String(14), unique=True, index=True)
    email: so.Mapped[Optional[str]] = so.mapped_column(sa.String(120), unique=True, index=True)
    telefone: so.Mapped[Optional[str]] = so.mapped_column(sa.String(30))
    ativo: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=True)

    # 🔹 Correção: ForeignKey referenciando tabelas reais
    cargo_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey("cargos.id"), index=True)
    secretaria_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey("secretarias.id"), index=True)

    cargo: so.Mapped["Cargo"] = so.relationship(back_populates="servidores")
    secretaria: so.Mapped["Secretaria"] = so.relationship(back_populates="servidores")
    usuario: so.Mapped["Usuario"] = so.relationship(back_populates="servidor", uselist=False)
