import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "notas.db"

def criar_tabela():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS notas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            arquivo TEXT,
            documento TEXT,
            cliente TEXT,
            transportadora TEXT,
            mensagem TEXT,
            data_emissao TEXT,
            chave_acesso TEXT
        )
    """)
    conn.commit()
    conn.close()

def inserir_nota(nota: dict):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO notas (arquivo, documento, cliente, transportadora, mensagem, data_emissao, chave_acesso)
        VALUES (?, ?, ?, ?, ?, ?,?)
    """, (
        nota["arquivo"],
        nota["documento"],
        nota["cliente"],
        nota["transportadora"],
        nota["mensagem"],
        nota["data_emissao"],
        nota["chave_acesso"]
    ))
    conn.commit()
    conn.close()

def buscar_nota_mais_recente(documento: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT arquivo, documento, cliente, transportadora, mensagem, data_emissao, chave_acesso
        FROM notas
        WHERE documento = ?
        ORDER BY datetime(data_emissao) DESC
        LIMIT 1
    """, (documento,))
    row = cur.fetchone()
    conn.close()

    if row:
        return {
            "arquivo": row[0],
            "documento": row[1],
            "cliente": row[2],
            "transportadora": row[3],
            "mensagem": row[4],
            "data_emissao": row[5],
            "chave_acesso": row[6],
        }
    return None
