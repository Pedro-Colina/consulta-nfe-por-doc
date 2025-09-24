from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD

# URL de conexão no formato async
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# Cria o engine async
engine = create_async_engine(
    DATABASE_URL,
    echo=False,       # colocar True se quiser debug SQL no console
    future=True
)

# Session local (cada request abre sua própria sessão)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

# Base para os modelos
Base = declarative_base()

# Dependência que pode ser usada nos endpoints
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
