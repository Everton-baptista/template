#!/usr/bin/env python3
import sys
import re
import argparse
from pathlib import Path

AGENT_TEMPLATE = '''from agno.agent import Agent
from app.agents.base import get_default_model
from app.storage.db_storage import get_agent_storage
from app.skills import get_workspace_skills
from app.tools import get_{tool_group}_tools

def get_{agent_func_name}_agent(model_id: str = None) -> Agent:
    """
    Agente Especialista {agent_name}.
    """
    return Agent(
        name="{agent_name}",
        model=get_default_model(model_id),
        tools=get_{tool_group}_tools(),
        skills=get_workspace_skills(),
        instructions=[
            "Você é o agente {agent_name}.",
            "Sua missão é atender as solicitações com precisão, clareza e alto nível profissional."
        ],
        markdown=True,
        db=get_agent_storage(table_name="{snake_name}_sessions"),
    )
'''

def to_snake_case(name: str) -> str:
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def main():
    parser = argparse.ArgumentParser(description="Gerador automático de novos Agentes Agno")
    parser.add_argument("--name", required=True, help="Nome do Agente (ex: FinancialAdvisor)")
    parser.add_argument("--tool-group", default="research", help="Grupo de ferramentas (research, data, devops, document, communication, media)")
    args = parser.parse_args()

    agent_name = args.name.strip()
    snake_name = to_snake_case(agent_name)
    if not snake_name.endswith("_agent"):
        snake_name += "_agent"
    
    agent_func_name = snake_name.replace("_agent", "")
    
    agents_dir = Path(__file__).parent.parent / "app" / "agents"
    file_path = agents_dir / f"{agent_func_name}.py"

    if file_path.exists():
        print(f"❌ Erro: O arquivo {file_path} já existe.")
        sys.exit(1)

    content = AGENT_TEMPLATE.format(
        agent_name=agent_name,
        agent_func_name=agent_func_name,
        snake_name=snake_name,
        tool_group=args.tool_group
    )

    file_path.write_text(content, encoding="utf-8")
    print(f"✅ Agente '{agent_name}' criado com sucesso em: {file_path}")
    print(f"👉 Lembre-se de importar 'get_{agent_func_name}_agent' em app/agents/__init__.py e app/api/routes.py")

if __name__ == "__main__":
    main()
