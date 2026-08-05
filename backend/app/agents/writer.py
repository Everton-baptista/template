from agno.agent import Agent
from app.agents.base import get_default_model
from app.tools.document_tools import get_document_tools
from app.storage.db_storage import get_agent_storage
from app.skills import get_workspace_skills

def get_writer_agent(model_id: str = None) -> Agent:
    """
    Agente Especialista em Redação e Comunicação com a skill 'executive-writing' integrada.
    """
    return Agent(
        name="WriterAgent",
        model=get_default_model(model_id),
        tools=get_document_tools(),
        skills=get_workspace_skills(),
        instructions=[
            "Você é um Redator Técnico e Comunicador Executivo Sênior.",
            "Aplique a skill 'executive-writing' para seguir a Pirâmide de Minto e redigir relatórios C-Level impecáveis.",
            "Utilize marcações Markdown apropriadas (títulos, listas, blocos de destaque).",
            "Garanta tom profissional, coesão e clareza impecáveis."
        ],
        markdown=True,
        db=get_agent_storage(table_name="writer_sessions"),
    )
