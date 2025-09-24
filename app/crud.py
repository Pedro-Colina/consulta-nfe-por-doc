from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Nota
from typing import Dict, Optional

async def inserir_nota(db: AsyncSession, nota: dict):
    # Verifica se já existe essa chave
    result = await db.execute(select(Nota).where(Nota.chave_acesso == nota["chave_acesso"]))
    existente = result.scalar_one_or_none()
    if existente:
        return existente  # evita duplicar

    nova_nota = Nota(**nota)
    db.add(nova_nota)
    await db.commit()
    await db.refresh(nova_nota)
    return nova_nota

async def buscar_nota_mais_recente(db: AsyncSession, documento: str) -> Optional[Nota]:
    result = await db.execute(
        select(Nota)
        .where(Nota.documento == documento)
        .order_by(Nota.data_emissao.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()
