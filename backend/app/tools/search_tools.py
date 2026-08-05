from agno.tools.duckduckgo import DuckDuckGoTools
from app.core.config import settings

def get_search_tools():
    """
    Retorna instâncias de ferramentas de busca na Web pré-configuradas.
    Se EXA_API_KEY ou TAVILY_API_KEY estiverem configuradas, ativa integrações estendidas.
    """
    tools = [
        DuckDuckGoTools(enable_search=True, enable_news=True, modifier="site:github.com OR site:stackoverflow.com OR site:arxiv.org")
    ]
    
    if settings.EXA_API_KEY:
        try:
            from agno.tools.exa import ExaTools
            tools.append(ExaTools(api_key=settings.EXA_API_KEY))
        except ImportError:
            pass

    return tools
