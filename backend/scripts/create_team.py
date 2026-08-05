#!/usr/bin/env python3
import sys
import re
import argparse
from pathlib import Path

TEAM_TEMPLATE = '''from agno.team import Team
from app.agents.base import get_default_model
from app.agents import get_researcher_agent, get_analyst_agent, get_writer_agent
from app.storage.db_storage import get_agent_storage

def get_{team_func_name}_team(model_id: str = None) -> Team:
    """
    Equipe Multiagente {team_name}.
    """
    researcher = get_researcher_agent(model_id)
    analyst = get_analyst_agent(model_id)
    writer = get_writer_agent(model_id)

    return Team(
        name="{team_name}",
        model=get_default_model(model_id),
        members=[researcher, analyst, writer],
        instructions=[
            "Você é o Líder da Equipe {team_name}.",
            "Coordene os membros da equipe e entregue uma resposta consolidada."
        ],
        markdown=True,
        db=get_agent_storage(table_name="{snake_name}_sessions"),
    )
'''

def to_snake_case(name: str) -> str:
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def main():
    parser = argparse.ArgumentParser(description="Gerador automático de novas Equipes Multiagentes Agno")
    parser.add_argument("--name", required=True, help="Nome da Equipe (ex: FinTechExecutiveTeam)")
    args = parser.parse_args()

    team_name = args.name.strip()
    snake_name = to_snake_case(team_name)
    if not snake_name.endswith("_team"):
        snake_name += "_team"
    
    team_func_name = snake_name.replace("_team", "")
    
    teams_dir = Path(__file__).parent.parent / "app" / "teams"
    file_path = teams_dir / f"{team_func_name}.py"

    if file_path.exists():
        print(f"❌ Erro: O arquivo {file_path} já existe.")
        sys.exit(1)

    content = TEAM_TEMPLATE.format(
        team_name=team_name,
        team_func_name=team_func_name,
        snake_name=snake_name
    )

    file_path.write_text(content, encoding="utf-8")
    print(f"✅ Equipe Multiagente '{team_name}' criada com sucesso em: {file_path}")
    print(f"👉 Lembre-se de importar 'get_{team_func_name}_team' em app/teams/__init__.py e app/api/routes.py")

if __name__ == "__main__":
    main()
