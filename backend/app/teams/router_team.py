from agno.team import Team
from app.agents.base import get_default_model
from app.teams.research_team import get_research_and_writing_team
from app.teams.dev_team import get_software_dev_team
from app.agents.analyst import get_analyst_agent
from app.storage.db_storage import get_agent_storage

def get_router_team(model_id: str = None) -> Team:
    """
    Roteador Inteligente Multiagente que classifica o pedido do usuário e o delega para a equipe ou agente mais apto.
    """
    research_team = get_research_and_writing_team(model_id)
    dev_team = get_software_dev_team(model_id)
    analyst = get_analyst_agent(model_id)

    return Team(
        name="RouterTeamManager",
        model=get_default_model(model_id),
        members=[research_team, dev_team, analyst],
        instructions=[
            "Você é um Roteador Inteligente e Orquestrador Geral de Agentes.",
            "Analise a solicitação recebida:",
            "- Se for sobre pesquisa, busca de notícias, tendências ou redação de relatórios -> Delegue para ResearchAndWritingTeamLeader.",
            "- Se for sobre codificação, refatoração, bugs, SQL ou scripts -> Delegue para SoftwareDevTeamLeader.",
            "- Se for sobre finanças, cotações de ações ou cálculos -> Delegue para AnalystAgent.",
            "Retorne a resposta final consolidada."
        ],
        markdown=True,
        db=get_agent_storage(table_name="router_team_sessions"),
    )
