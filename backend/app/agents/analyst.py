from agno.agent import Agent
from app.agents.base import get_default_model
from app.tools.data_tools import get_data_tools
from app.tools.financial_tools import get_financial_tools
from app.storage.db_storage import get_agent_storage
from app.skills import get_workspace_skills

def get_analyst_agent(model_id: str = None) -> Agent:
    """
    Agente Especialista em Análise Quantitativa e de Dados com a skill 'data-analysis' integrada.
    """
    tools = get_data_tools() + [get_financial_tools()]
    return Agent(
        name="AnalystAgent",
        model=get_default_model(model_id),
        tools=tools,
        skills=get_workspace_skills(),
        instructions=[
            "Você é um Analista Quantitativo e de Dados Sênior.",
            "Aplique a skill 'data-analysis' para calcular estatísticas descritivas, processar dados e gerar relatórios numéricos.",
            "Apresente análises estruturadas com métricas chave, tabelas e interpretações acionáveis."
        ],
        markdown=True,
        db=get_agent_storage(table_name="analyst_sessions"),
    )
