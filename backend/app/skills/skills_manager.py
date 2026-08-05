import os
from pathlib import Path
from typing import Optional, List
from agno.skills import LocalSkills, Skills

def get_workspace_skills(skill_names: Optional[List[str]] = None) -> Optional[LocalSkills]:
    """
    Carrega skills locais configuradas no diretório de skills (.agents/skills/ ou backend/app/skills/catalog/).
    """
    skills_dir = Path(__file__).parent.parent.parent.parent / ".agents" / "skills"
    
    if not skills_dir.exists():
        skills_dir = Path(__file__).parent / "catalog"

    if not skills_dir.exists():
        return None

    try:
        return LocalSkills(directory=skills_dir)
    except Exception as e:
        print(f"Aviso ao carregar LocalSkills ({skills_dir}): {e}")
        return None
