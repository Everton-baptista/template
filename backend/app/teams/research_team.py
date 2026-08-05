from agno.team import Team
from app.agents.base import get_default_model
from app.agents.researcher import get_researcher_agent
from app.agents.analyst import get_analyst_agent
from app.agents.writer import get_writer_agent
from app.storage.db_storage import get_agent_storage

def get_research_and_writing_team(model_id: str = None) -> Team:
    """
    Equipe Multiagente composta por Líder de Pesquisa (Manager), Pesquisador Web, Analista e Redator.
    """
    researcher = get_researcher_agent(model_id)
    analyst = get_analyst_agent(model_id)
    writer = get_writer_agent(model_id)

    return Team(
        name="ResearchAndWritingTeamLeader",
        model=get_default_model(model_id),
        members=[researcher, analyst, writer],
        instructions=[
            "Você é o Líder de uma Equipe de Elite de Pesquisa e Redação.",
            "Delegue a coleta de fatos ao ResearcherAgent.",
            "Delegue análises de dados/finanças ao AnalystAgent.",
            "Delegue a formatação e síntese final ao WriterAgent.",
            "Coordene a execução e apresente uma resposta consolidada de altíssima qualidade."
        ],
        markdown=True,
        db=get_agent_storage(table_name="research_team_sessions"),
    )
