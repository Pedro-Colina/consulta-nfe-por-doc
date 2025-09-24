from fastapi import FastAPI
from mangum import Mangum  # adaptador para serverless

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API rodando no Vercel com PostgreSQL!"}

# Adaptador para o Vercel/Lambda
handler = Mangum(app)
