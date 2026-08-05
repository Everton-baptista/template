from agno.models.openai import OpenAIChat
from agno.models.anthropic import Claude
from agno.models.google import Gemini
from agno.models.groq import Groq
from app.core.config import settings

def get_default_model(model_id: str = None, provider: str = None):
    """
    Retorna uma instância de LLM do Agno baseada no provedor e ID especificados ou globais.
    """
    target_provider = (provider or settings.DEFAULT_MODEL_PROVIDER).lower()
    target_model_id = model_id or settings.DEFAULT_MODEL_ID

    if target_provider == "openai":
        return OpenAIChat(id=target_model_id, api_key=settings.OPENAI_API_KEY)
    elif target_provider == "anthropic":
        return Claude(id=target_model_id or "claude-3-5-sonnet-20241022", api_key=settings.ANTHROPIC_API_KEY)
    elif target_provider == "google" or target_provider == "gemini":
        return Gemini(id=target_model_id or "gemini-2.0-flash", api_key=settings.GEMINI_API_KEY)
    elif target_provider == "groq":
        return Groq(id=target_model_id or "llama-3.3-70b-versatile", api_key=settings.GROQ_API_KEY)
    else:
        return OpenAIChat(id="gpt-4o-mini", api_key=settings.OPENAI_API_KEY)
