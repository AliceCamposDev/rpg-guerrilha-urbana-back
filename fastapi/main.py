from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from config import init_vault
from config import get_logger
from routes import graph, notes, health

logger = get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager"""
    logger.info("Iniciando aplicação...")
    try:
        init_vault()
    except Exception as e:
        logger.error(f"Vault não carregado: {e}")
    yield
    logger.info("Encerrando aplicação...")


app = FastAPI(
    title="Obsidian Vault API",
    description="API para visualizar e navegar pelo seu vault Obsidian",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://alicecamposdev.github.io/","https://alicecamposdev.github.io/*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


templates = Jinja2Templates(directory="./templates")

app.include_router(graph.router, prefix="/api")
app.include_router(notes.router, prefix="/api")
# app.include_router(search.router, prefix="/api")
app.include_router(health.router, prefix="/api")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Página inicial com Swagger de cria"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api")
async def api_root():
    """Endpoint raiz da API"""
    return {
        "message": "API do Vault Obsidian",
        "endpoints": {
            "/api/graph": "Retorna o grafo de conexões entre notas",
            "/api/notes": "Lista todas as notas",
            "/api/note/{note_name}": "Retorna conteúdo de uma nota específica",
            "/api/health": "Verifica o status do servidor",
            "/api/search": "Busca notas por termo",
            "/api/docs": "Documentação Swagger",
            "/api/redoc": "Documentação ReDoc",
        },
    }

