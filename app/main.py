#cria a aplicação
# registra rotas
# inicia o servidor

from fastapi import FastAPI
from app.routes.summarize import router as summarize_router

app = FastAPI(title="Docka")

app.include_router(summarize_router, prefix="/summarize")

