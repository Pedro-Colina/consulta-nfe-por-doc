import psycopg2
from app.config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
from typing import Optional, Dict

def get_db_connection():
    """
    Estabelece e retorna uma conexão com o banco de dados PostgreSQL.
    """
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        # Em produção, você pode querer registrar este erro
        return None

def criar_tabela():
    """
    Cria a tabela de notas fiscais se ela ainda não existir.
    """
    conn = get_db_connection()
    if conn is None:
        return

    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS notas (
                    id SERIAL PRIMARY KEY,
                    arquivo TEXT,
                    documento TEXT,
                    cliente TEXT,
                    transportadora TEXT,
                    mensagem TEXT,
                    data_emissao TEXT,
                    chave_acesso TEXT
                );
            """)
        conn.commit()
        print("Tabela 'notas' verificada/criada com sucesso.")
    except Exception as e:
        print(f"Erro ao criar a tabela: {e}")
    finally:
        if conn:
            conn.close()

def inserir_nota(nota: Dict):
    """
    Insere uma nota fiscal no banco de dados.
    """
    conn = get_db_connection()
    if conn is None:
        return

    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO notas (
                    arquivo, documento, cliente, transportadora,
                    mensagem, data_emissao, chave_acesso
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                nota.get("arquivo"),
                nota.get("documento"),
                nota.get("cliente"),
                nota.get("transportadora"),
                nota.get("mensagem"),
                nota.get("data_emissao"),
                nota.get("chave_acesso")
            ))
        conn.commit()
    except Exception as e:
        print(f"Erro ao inserir nota fiscal: {e}")
    finally:
        if conn:
            conn.close()

def buscar_nota_mais_recente(documento: str) -> Optional[Dict]:
    """
    Busca a nota fiscal mais recente com base no CNPJ ou CPF.
    """
    conn = get_db_connection()
    if conn is None:
        return None

    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    arquivo, documento, cliente, transportadora,
                    mensagem, data_emissao, chave_acesso
                FROM
                    notas
                WHERE
                    documento = %s
                ORDER BY
                    data_emissao DESC
                LIMIT 1;
            """, (documento,))

            result = cur.fetchone()

            if result:
                # Mapeia o resultado para um dicionário para manter a compatibilidade
                columns = [desc[0] for desc in cur.description]
                return dict(zip(columns, result))

    except Exception as e:
        print(f"Erro ao buscar nota fiscal: {e}")
    finally:
        if conn:
            conn.close()
    return None
