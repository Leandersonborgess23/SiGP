from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Boolean, Integer, DateTime, ForeignKey
from app import db

class Documento(db.Model):
    __tablename__ = "documentos"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    descricao: Mapped[Optional[str]] = mapped_column(Text)
    categoria: Mapped[str] = mapped_column(String(100), nullable=False)
    arquivo: Mapped[str] = mapped_column(String(300), nullable=False)
    criado_por: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="documentos")
    secretaria_id: Mapped[Optional[int]] = mapped_column(ForeignKey("secretarias.id"))
    secretaria: Mapped[Optional["Secretaria"]] = relationship("Secretaria", back_populates="documentos")
    privado: Mapped[bool] = mapped_column(Boolean, default=False)
    tags: Mapped[Optional[str]] = mapped_column(String(200))
    data_criacao: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    atualizado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
