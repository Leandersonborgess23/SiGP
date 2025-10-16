from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so
from typing import Optional
from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
    __tablename__ = "usuarios"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True, nullable=False)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    role: so.Mapped[Optional[str]] = so.mapped_column(sa.String(30), default="servidor")

    # 👇 Aqui está a correção importante
    servidor_id: so.Mapped[Optional[int]] = so.mapped_column(
        sa.ForeignKey("servidores.id"), unique=True, index=True, nullable=True
    )

    # relacionamento declarado por string — sem precisar importar Servidor
    servidor: so.Mapped["Servidor"] = so.relationship(back_populates="usuario")
