from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import logger
from app.api.routes import router as api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="API FastAPI de Alta Performance para Agentes e Multiagentes construída com o Framework Agno. Suporta REST, SSE e WebSockets.",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configuração de CORS para comunicação fluida com Frontend Next.js e Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas v1
app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    logger.info(f"🚀 {settings.PROJECT_NAME} iniciado com sucesso no ambiente '{settings.ENV}'.")
    logger.info("📡 Protocolos Habilitados: REST (JSON), SSE (Streaming), WebSockets (Bidirecional).")

@app.get("/")
async def root():
    return {
        "message": f"Bem-vindo ao {settings.PROJECT_NAME}!",
        "docs": "/docs",
        "version": "1.0.0",
        "protocols": ["REST", "SSE", "WebSocket"]
    }
