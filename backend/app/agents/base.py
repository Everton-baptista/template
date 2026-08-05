import os
from agno.models.openai import OpenAIChat
from agno.models.anthropic import Claude
from agno.models.google import Gemini
from agno.models.groq import Groq
from app.core.config import settings

def get_default_model(model_id: str = None, provider: str = None):
    """
    Retorna uma instância de LLM do Agno baseada no provedor e ID especificados ou globais.
    Todos os agentes são definidos na pasta app/agents/ usando esta fábrica de modelos.
    """
    target_provider = (provider or settings.DEFAULT_MODEL_PROVIDER).lower()
    target_model_id = model_id or settings.DEFAULT_MODEL_ID

    openai_key = os.getenv("OPENAI_API_KEY") or settings.OPENAI_API_KEY
    anthropic_key = os.getenv("ANTHROPIC_API_KEY") or settings.ANTHROPIC_API_KEY
    gemini_key = os.getenv("GEMINI_API_KEY") or settings.GEMINI_API_KEY
    groq_key = os.getenv("GROQ_API_KEY") or settings.GROQ_API_KEY

    if target_provider == "openai":
        return OpenAIChat(id=target_model_id, api_key=openai_key)
    elif target_provider == "anthropic":
        return Claude(id=target_model_id or "claude-3-5-sonnet-20241022", api_key=anthropic_key)
    elif target_provider in ("google", "gemini"):
        return Gemini(id=target_model_id or "gemini-2.0-flash", api_key=gemini_key)
    elif target_provider == "groq":
        return Groq(id=target_model_id or "llama-3.3-70b-versatile", api_key=groq_key)
    else:
        return OpenAIChat(id=target_model_id or "gpt-4o-mini", api_key=openai_key)

