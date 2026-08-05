from agno.agent import Agent
from agno.team import Team
from app.agents.base import get_default_model
from app.agents.coder import get_coder_agent
from app.storage.db_storage import get_agent_storage

def get_software_dev_team(model_id: str = None) -> Team:
    """
    Equipe Multiagente de Desenvolvimento de Software.
    """
    coder = get_coder_agent(model_id)

    reviewer = Agent(
        name="CodeReviewer",
        model=get_default_model(model_id),
        instructions=[
            "Você é um Revisor de Código Sênior focado em segurança, performance e arquitetura.",
            "Inspecione o código gerado, identifique potenciais vulnerabilidades, bugs ou más práticas."
        ],
        markdown=True
    )

    return Team(
        name="SoftwareDevTeamLeader",
        model=get_default_model(model_id),
        members=[coder, reviewer],
        instructions=[
            "Você é o Arquiteto de Software Líder.",
            "Coordene a geração de código com o CoderAgent e garanta a revisão de qualidade com o CodeReviewer.",
            "Entregue soluções de código completas, seguras e bem documentadas."
        ],
        markdown=True,
        db=get_agent_storage(table_name="dev_team_sessions"),
    )
