from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from contextlib import asynccontextmanager
import traceback
import tempfile
import aiofiles
import os
from typing import List
from .database import get_db, Base, engine
from .crud import buscar_nota_mais_recente
from .utils import processa_xml  # Certifique-se de que processa_xml está definido em xml_utils.py
from .models import Nota  # Adiciona a importação do modelo Nota

# Lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield
    except Exception as e:
        print("Erro no lifespan ao inicializar o DB:")
        traceback.print_exc()
        raise
    finally:
        await engine.dispose()

# AQUI: o Vercel procura esse objeto
app = FastAPI(
    title="API de Consulta de NF-e",
    description="Consulta a NF-e mais recente com base no CPF ou CNPJ do cliente",
    version="1.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {"message": "API rodando no Vercel + Neon PostgreSQL!"}

@app.get("/notas/{documento}")
async def buscar_nota_mais_recente_por_documento(documento: str, db: AsyncSession = Depends(get_db)):
    """
    Busca a nota fiscal mais recente com base no CPF/CNPJ do cliente.
    """
    return await buscar_nota_mais_recente(db, documento)

@app.post("/notas/upload-lote")
async def upload_lote(
    files: List[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db)
):
    notas_inseridas = []
    erros = []
    duplicados = []

    for file in files:
        try:
            # salva temporariamente usando aiofiles
            tmp_fd, tmp_path = tempfile.mkstemp(suffix=".xml")
            os.close(tmp_fd)  # Fecha o descritor de arquivo imediatamente

            contents = await file.read()
            async with aiofiles.open(tmp_path, 'wb') as tmp:
                await tmp.write(contents)

            nota_dict = processa_xml(tmp_path, file.filename)
            os.remove(tmp_path)

            if not nota_dict:
                erros.append({"arquivo": file.filename, "erro": "XML inválido"})
                continue

            # Verifica duplicados
            stmt = select(Nota).where(Nota.chave_acesso == nota_dict["chave_acesso"])
            result = await db.execute(stmt)
            existente = result.scalar_one_or_none()

            if existente:
                duplicados.append(nota_dict["chave_acesso"])
                continue

            nova_nota = Nota(**nota_dict)
            db.add(nova_nota)
            notas_inseridas.append(nota_dict)

        except Exception as e:
            erros.append({"arquivo": file.filename, "erro": str(e)})

    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao salvar no banco: {str(e)}")

    return {
        "sucesso": len(notas_inseridas),
        "duplicados": len(duplicados),
        "falhas": len(erros),
        "notas_inseridas": notas_inseridas,
        "erros": erros
    }
