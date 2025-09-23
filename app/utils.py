import xml.etree.ElementTree as ET
import os
from datetime import datetime
from typing import Optional
from .config import XML_FOLDER
from .mensagens import get_mensagem

noinf = "Não informado"

def local_name(tag: str) -> str:
    """Retorna o nome local da tag removendo namespace se existir."""
    return tag.split("}")[-1] if "}" in tag else tag

def find_tag(root: ET.Element, path: str) -> Optional[ET.Element]:
    """Procura por tags ignorando namespaces."""
    parts = path.split("/")
    current = root
    for part in parts:
        found = None
        for el in current.iter():
            if local_name(el.tag) == part:
                found = el
                break
        if found is None:
            return None
        current = found
    return current

def get_access_key(root: ET.Element) -> Optional[str]:
    """Extrai a chave de acesso da NF-e do atributo Id de infNFe."""
    infnfe = find_tag(root, "infNFe")
    if infnfe is not None:
        chave = infnfe.attrib.get("Id", "")
        if chave.startswith("NFe"):
            chave = chave[3:]  # remove o prefixo "NFe"
        return chave if chave else None
    return noinf

def get_client_document(root: ET.Element) -> Optional[str]:
    cpf_tag = find_tag(root, "dest/CPF")
    cnpj_tag = find_tag(root, "dest/CNPJ")
    if cpf_tag is not None:
        return cpf_tag.text
    if cnpj_tag is not None:
        return cnpj_tag.text
    return None

def get_emission_date(root: ET.Element) -> Optional[str]:
    data_tag = find_tag(root, "ide/dhEmi")  # corrigido (sem nfe:)
    if data_tag is not None and data_tag.text:
        try:
            return datetime.fromisoformat(data_tag.text).isoformat()
        except Exception:
            # fallback: tenta cortar só data
            return data_tag.text[:10]
    return None

def text_in_tag(tag: str, root) -> str:
    found_tag = find_tag(root, tag)
    return found_tag.text if found_tag is not None else noinf


def processa_xml(filepath: str, filename: str, documento_target: Optional[str] = None):
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()

        doc_cliente = get_client_document(root)
        if documento_target and doc_cliente != documento_target:
            return None

        nome_cliente = text_in_tag("dest/xNome", root)
        transportadora = text_in_tag("transp/transporta/xNome", root)
        n_nf = text_in_tag("ide/nNF", root)
        cnpj = text_in_tag("emit/CNPJ", root)
        chave_acess = get_access_key(root)
        data_emissao = get_emission_date(root)
        mensagem = get_mensagem(transportadora, n_nf, doc_cliente, cnpj)

        nota = {
            "arquivo": filename,
            "documento": doc_cliente or noinf,
            "cliente": nome_cliente,
            "transportadora": transportadora,
            "mensagem": mensagem,
            "data_emissao": data_emissao or noinf,
            "chave_acesso": chave_acess
        }

        return nota
    except Exception as e:
        print(f"Erro ao processar {filename}: {e}")
        return None

def buscar_nota_mais_recente_por_documento(documento: str):
    notas = []
    for filename in os.listdir(XML_FOLDER):
        if filename.endswith(".xml"):
            filepath = os.path.join(XML_FOLDER, filename)
            nota = processa_xml(filepath, filename, documento)
            if nota:
                notas.append(nota)

    if not notas:
        return None

    notas_validas = [n for n in notas if n["data_emissao"] != noinf]
    if notas_validas:
        return max(notas_validas, key=lambda x: x["data_emissao"])
    else:
        return notas[-1]
