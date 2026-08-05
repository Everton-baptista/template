from typing import List, Optional
from app.core.config import settings

def get_dalle_tools(api_key: Optional[str] = None):
    """Ferramenta de geração e edição de imagens via OpenAI DALL-E."""
    target_key = api_key or settings.OPENAI_API_KEY
    if not target_key:
        return None
    try:
        from agno.tools.dalle import DalleTools
        return DalleTools(api_key=target_key)
    except Exception as e:
        print(f"DalleTools indisponível: {e}")
        return None

def get_youtube_tools():
    """Ferramenta de extração de dados, legendas e transcrição de vídeos do YouTube."""
    try:
        from agno.tools.youtube import YouTubeTools
        return YouTubeTools()
    except Exception as e:
        print(f"YouTubeTools indisponível: {e}")
        return None

def get_media_tools() -> List:
    """
    Retorna o conjunto de ferramentas de mídia, imagens e vídeo.
    """
    tools = []
    
    dalle = get_dalle_tools()
    if dalle:
        tools.append(dalle)
        
    yt = get_youtube_tools()
    if yt:
        tools.append(yt)

    return tools
