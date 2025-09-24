from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Integer, TIMESTAMP
from datetime import datetime
from .database import Base

class Nota(Base):
    __tablename__ = "notas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    arquivo: Mapped[str] = mapped_column(Text)
    documento: Mapped[str] = mapped_column(String(50), index=True)
    cliente: Mapped[str] = mapped_column(Text)
    transportadora: Mapped[str] = mapped_column(Text)
    mensagem: Mapped[str] = mapped_column(Text)
    data_emissao: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    chave_acesso: Mapped[str] = mapped_column(Text, unique=True)
