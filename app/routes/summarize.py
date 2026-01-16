# Aqui eu importo o que vou precisar do FastAPI
# APIRouter: para organizar minhas rotas fora do main.py
# UploadFile: representa o arquivo que o usuário envia
# File: indica que esse parâmetro vem de um upload
# HTTPException: uso para retornar erros controlados pela API
from fastapi import APIRouter, UploadFile, File, HTTPException

# Biblioteca padrão do Python para trabalhar com pastas e caminhos
import os

# Biblioteca para copiar arquivos de forma segura e eficiente
import shutil

# Biblioteca para gerar IDs únicos para os arquivos
import uuid

# Crio um router para não precisar colocar todas as rotas no main.py
# Isso deixa o projeto mais organizado
router = APIRouter()

# Pasta onde os arquivos enviados vão ser salvos temporariamente
UPLOAD_DIR = "temp"

# Garanto que a pasta exista, se não existir eu crio
# exist_ok=True evita erro se a pasta já existir
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Crio o endpoint POST na raiz do router
# Ele vai receber arquivos PDF enviados pelo usuário
@router.post("/")
async def summarize(file: UploadFile = File(...)):
    """
    Essa função é responsável por:
    1. Receber o arquivo enviado pelo usuário
    2. Validar se é PDF
    3. Salvar o arquivo em disco na pasta 'temp'
    4. Retornar uma mensagem confirmando que deu certo

    Ainda NÃO estou fazendo resumo do conteúdo, só salvando o arquivo.
    """

    # Validação básica: se o arquivo não for PDF, retorno erro
    if file.content_type != "application/pdf":
        # Aqui eu uso HTTPException para retornar um erro 400 para o usuário
        # Isso evita que arquivos errados sejam salvos
        raise HTTPException(
            status_code=400,
            detail="Apenas arquivos PDF são permitidos"
        )

    # Gero um ID único para o arquivo, assim evito sobrescrever arquivos
    file_id = str(uuid.uuid4())

    # Crio o caminho completo do arquivo usando a pasta e o ID único
    # Exemplo: temp/123e4567-89ab-meuarquivo.pdf
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")

    # Abro o arquivo em modo escrita binária ("wb")
    # file.file.read() lê todo o conteúdo do UploadFile
    # Aqui estou salvando o arquivo enviado na minha pasta temp
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    # Retorno uma resposta simples só para confirmar que deu certo
    # Isso ajuda a validar que o upload funcionou
    return {
        "message": "Upload realizado com sucesso",
        "file_path": file_path
    }
