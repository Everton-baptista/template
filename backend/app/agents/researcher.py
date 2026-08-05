from agno.agent import Agent
from app.agents.base import get_default_model
from app.tools.research_tools import get_research_tools
from app.storage.db_storage import get_agent_storage
from app.skills import get_workspace_skills

def get_researcher_agent(model_id: str = None) -> Agent:
    """
    Agente Especialista em Pesquisa e Coleta de Informações com a skill 'web-research' integrada.
    """
    return Agent(
        name="ResearcherAgent",
        model=get_default_model(model_id),
        tools=get_research_tools(),
        skills=get_workspace_skills(),
        instructions=[
            "Você é um Pesquisador Sênior e Especialista em Coleta de Informações na Web.",
            "Aplique a skill 'web-research' para realizar pesquisas profundas com triangulação de fontes e fatos.",
            "Sempre cite fontes confiáveis e inclua URLs de referência quando disponível.",
            "Apresente seus achados em formato Markdown limpo e objetivo."
        ],
        markdown=True,
        db=get_agent_storage(table_name="researcher_sessions"),
    )
