# 📦 API de Consulta de NF-e

Essa API permite consultar a **nota fiscal mais recente** de um cliente com base no CPF ou CNPJ e retorna:
- Nome do cliente
- Transportadora
- Mensagem personalizada
- Data de emissão
- Nome do arquivo XML

---

## 🚀 Como rodar

1. Crie um diretório e extraia o `.zip`:

   ```bash
   unzip projeto-nfe-api.zip
   cd projeto-nfe-api
   ```

2. Crie o ambiente virtual (opcional mas recomendado):

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate    # Windows
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure a pasta com os XMLs:
   - No arquivo `app/config.py` altere a linha:

     ```python
     XML_FOLDER = "C:/notas"
     ```

   ou use variável de ambiente:

   ```bash
   export XML_FOLDER="/caminho/para/xmls"
   ```

5. Rode a API:

   ```bash
   uvicorn app.main:app --reload
   ```

6. Acesse a documentação:

   [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔎 Exemplo de consulta

```
GET http://localhost:8000/consulta/12345678901
```

Resposta:

```json
{
  "arquivo": "NF456.xml",
  "documento": "12345678901",
  "cliente": "Fulano da Silva",
  "transportadora": "Transportadora ABC LTDA",
  "mensagem": "A Transportadora ABC entrará em contato para agendar a entrega.",
  "data_emissao": "2023-08-15T15:30:00"
}
```
