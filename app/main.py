from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from .utils import buscar_nota_mais_recente_por_documento
import os
from app.utils import processa_xml
from app.config import XML_FOLDER
from app.database import buscar_nota_mais_recente, criar_tabela
import importar_xmls

app = FastAPI(
    title="API de Consulta de NF-e",
    description="Consulta a NF-e mais recente com base no CPF ou CNPJ do cliente",
    version="1.0"
)

def importar_xml():
    criar_tabela()  # garante que a tabela existe

    arquivos_processados = 0
    for filename in os.listdir(XML_FOLDER):
        if filename.endswith(".xml"):
            filepath = os.path.join(XML_FOLDER, filename)

            # Aqui não passamos documento alvo, então forçamos processamento de todos
            nota = processa_xml(filepath, filename, documento_target=None)

            if nota:
                arquivos_processados += 1

    print(f"Importação concluída! {arquivos_processados} arquivos processados.")

if __name__ == "__main__":
    importar_xml()


@app.get("/consulta/{documento}", tags=["Consultas"])
def consulta_por_documento(documento: str):
    resultado = buscar_nota_mais_recente(documento)
    if resultado:
        return resultado
    return {"message": "Nenhuma nota encontrada para esse CPF/CNPJ"}

@app.post("/importar", tags=["Importar XML"])
def importar_notas():
    """
    Importa os XMLs da pasta para o banco de dados.
    """
    msg = importar_xmls.importar_xmls()
    return {"mensagem": msg}
