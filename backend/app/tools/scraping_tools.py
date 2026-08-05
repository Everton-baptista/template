from typing import List, Optional
from app.core.config import settings

def get_newspaper4k_tools():
    """Ferramenta de extração, parsing e sumarização de artigos de notícias via Newspaper4k."""
    try:
        from agno.tools.newspaper4k import Newspaper4kTools
        return Newspaper4kTools()
    except Exception as e:
        print(f"Newspaper4kTools indisponível: {e}")
        return None

def get_website_tools():
    """Ferramenta de leitura e raspagem direta do conteúdo HTML/Texto de websites."""
    try:
        from agno.tools.website import WebsiteTools
        return WebsiteTools()
    except Exception as e:
        print(f"WebsiteTools indisponível: {e}")
        return None

def get_firecrawl_tools(api_key: Optional[str] = None):
    """Ferramenta avançada de crawling e scraping de websites via Firecrawl API."""
    target_key = api_key or getattr(settings, "FIRECRAWL_API_KEY", None)
    if not target_key:
        return None
    try:
        from agno.tools.firecrawl import FirecrawlTools
        return FirecrawlTools(api_key=target_key)
    except Exception as e:
        print(f"FirecrawlTools indisponível: {e}")
        return None

def get_scraping_tools() -> List:
    """
    Retorna o conjunto consolidado de ferramentas de extração e raspagem web.
    """
    tools = []
    
    newspaper = get_newspaper4k_tools()
    if newspaper:
        tools.append(newspaper)
        
    website = get_website_tools()
    if website:
        tools.append(website)

    firecrawl = get_firecrawl_tools()
    if firecrawl:
        tools.append(firecrawl)

    return tools
