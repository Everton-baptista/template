from agno.agent import Agent
from app.agents.base import get_default_model
from app.tools.devops_tools import get_devops_tools
from app.storage.db_storage import get_agent_storage
from app.skills import get_workspace_skills

def get_coder_agent(model_id: str = None) -> Agent:
    """
    Agente Especialista em Engenharia de Software com a skill 'code-review' integrada.
    """
    return Agent(
        name="CoderAgent",
        model=get_default_model(model_id),
        tools=get_devops_tools(),
        skills=get_workspace_skills(),
        instructions=[
            "Você é um Engenheiro de Software Principal especialista em Python, TypeScript, SQL e arquitetura.",
            "Aplique a skill 'code-review' para auditar segurança OWASP, aplicar princípios SOLID e escrever código impecável.",
            "Forneça explicações concisas juntamente com blocos de código com sintaxe apropriada."
        ],
        markdown=True,
        db=get_agent_storage(table_name="coder_sessions"),
    )
