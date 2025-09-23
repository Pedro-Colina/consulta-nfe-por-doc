import os
import sqlite3
from app.utils import processa_xml
from app.config import XML_FOLDER
from app.database import criar_tabela, DB_PATH

def carregar_arquivos_existentes():
    """Retorna um set com os nomes dos arquivos já cadastrados no banco."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT arquivo FROM notas")
    arquivos_existentes = set(row[0] for row in cur.fetchall())
    conn.close()
    return arquivos_existentes

def processar_novos_xmls(arquivos_existentes):
    """Percorre a pasta de XMLs e processa apenas os novos arquivos."""
    novas_notas = []

    for filename in os.listdir(XML_FOLDER):
        if not filename.endswith(".xml"):
            continue

        if filename in arquivos_existentes:
            continue  # já cadastrado

        filepath = os.path.join(XML_FOLDER, filename)
        nota = processa_xml(filepath, filename)

        if nota:
            novas_notas.append((
                nota["arquivo"],
                nota["documento"],
                nota["cliente"],
                nota["transportadora"],
                nota["mensagem"],
                nota["data_emissao"],
                nota['chave_acesso']
            ))

    return novas_notas

def salvar_novas_notas(novas_notas):
    """Insere as novas notas no banco de dados em batch."""
    if not novas_notas:
        return 0

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executemany("""
        INSERT INTO notas (arquivo, documento, cliente, transportadora, mensagem, data_emissao, chave_acesso)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, novas_notas)
    conn.commit()
    conn.close()

    return len(novas_notas)

def importar_xmls():
    """Função principal: importa os XMLs novos para o banco SQLite."""
    criar_tabela()  # garante que a tabela existe
    arquivos_existentes = carregar_arquivos_existentes()
    novas_notas = processar_novos_xmls(arquivos_existentes)
    quantidade = salvar_novas_notas(novas_notas)
    text = "Todos os dados ja estão cadastrados!"
    if(quantidade > 0):
        text = f"Importação concluída! {quantidade} arquivos novos processados."
        print(text)
        return text
    else:
        print(text)
        return text

if __name__ == "__main__":
    importar_xmls()
