from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db, Base, engine
from .crud import buscar_nota_mais_recente, inserir_nota
from . import crud, models
import asyncio

app = FastAPI()

# Criar tabelas (apenas para testes — em produção use Alembic!)
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_models())

@app.get("/")
async def root():
    return {"message": "API rodando no Vercel + Neon PostgreSQL!"}

@app.post("/notas/")
async def criar_nota(nota: dict, db: AsyncSession = Depends(get_db)):
    return await inserir_nota(db, nota)

@app.get("/notas/{documento}")
async def buscar_nota_mais_recente_por_documento(documento: str, db: AsyncSession):
    return await buscar_nota_mais_recente(db, documento)
