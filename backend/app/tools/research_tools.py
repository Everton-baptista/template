from typing import List, Optional
from agno.tools.duckduckgo import DuckDuckGoTools
from app.core.config import settings

def get_duckduckgo_tools() -> DuckDuckGoTools:
    """Ferramenta de busca genérica na Web e notícias via DuckDuckGo."""
    return DuckDuckGoTools(enable_search=True, enable_news=True)

def get_arxiv_tools():
    """Ferramenta de pesquisa de artigos científicos e acadêmicos no ArXiv."""
    try:
        from agno.tools.arxiv import ArxivTools
        return ArxivTools()
    except Exception as e:
        print(f"ArxivTools indisponível: {e}")
        return None

def get_wikipedia_tools():
    """Ferramenta de pesquisa e consulta enciclopédica na Wikipedia."""
    try:
        from agno.tools.wikipedia import WikipediaTools
        return WikipediaTools()
    except Exception as e:
        print(f"WikipediaTools indisponível: {e}")
        return None

def get_hackernews_tools():
    """Ferramenta de busca por postagens e notícias no HackerNews."""
    try:
        from agno.tools.hackernews import HackerNewsTools
        return HackerNewsTools()
    except Exception as e:
        print(f"HackerNewsTools indisponível: {e}")
        return None

def get_tavily_tools(api_key: Optional[str] = None):
    """Ferramenta de pesquisa otimizada para LLMs via Tavily API."""
    target_key = api_key or settings.TAVILY_API_KEY
    if not target_key:
        return None
    try:
        from agno.tools.tavily import TavilyTools
        return TavilyTools(api_key=target_key)
    except Exception as e:
        print(f"TavilyTools indisponível: {e}")
        return None

def get_exa_tools(api_key: Optional[str] = None):
    """Ferramenta de pesquisa neural via Exa AI API."""
    target_key = api_key or settings.EXA_API_KEY
    if not target_key:
        return None
    try:
        from agno.tools.exa import ExaTools
        return ExaTools(api_key=target_key)
    except Exception as e:
        print(f"ExaTools indisponível: {e}")
        return None

def get_research_tools() -> List:
    """
    Retorna o conjunto consolidado de ferramentas de pesquisa e investigação ativas.
    """
    tools = [get_duckduckgo_tools()]
    
    arxiv = get_arxiv_tools()
    if arxiv:
        tools.append(arxiv)
        
    wiki = get_wikipedia_tools()
    if wiki:
        tools.append(wiki)
        
    hn = get_hackernews_tools()
    if hn:
        tools.append(hn)

    tavily = get_tavily_tools()
    if tavily:
        tools.append(tavily)

    exa = get_exa_tools()
    if exa:
        tools.append(exa)

    return tools
