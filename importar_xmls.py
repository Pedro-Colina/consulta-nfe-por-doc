import os
import asyncio
from app.utils import processa_xml
from app.database import get_db, AsyncSessionLocal
from app.crud import inserir_nota
from app.config import XML_FOLDER

async def importar_xmls():
    async with AsyncSessionLocal() as db:
        for filename in os.listdir(XML_FOLDER):
            if filename.endswith(".xml"):
                filepath = os.path.join(XML_FOLDER, filename)
                nota = processa_xml(filepath, filename)
                if nota:
                    try:
                        await inserir_nota(db, nota)
                        print(f"✅ Importado: {filename}")
                    except Exception as e:
                        print(f"⚠️ Erro ao importar {filename}: {e}")

if __name__ == "__main__":
    asyncio.run(importar_xmls())
