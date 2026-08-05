#!/usr/bin/env python3
import sys
import argparse
from pathlib import Path

SKILL_TEMPLATE = '''---
name: {skill_name}
description: "{description}"
---

# Skill: {title}

Ao executar tarefas relacionadas a esta skill, siga este protocolo:

## 1. Diretrizes Principais
- Siga as regras específicas de negócio.
- Aplique o padrão de qualidade e validação estrita.

## 2. Formato da Resposta
- Apresente a resposta estruturada em Markdown com títulos limpos e tópicos objetivos.
'''

def main():
    parser = argparse.ArgumentParser(description="Gerador automático de novas Skills para Agentes")
    parser.add_argument("--name", required=True, help="Nome da Skill em kebab-case (ex: sentiment-analysis)")
    parser.add_argument("--description", default="Skill de análise e instrução especializada.", help="Descrição da Skill")
    args = parser.parse_args()

    skill_name = args.name.strip().lower().replace("_", "-")
    title = skill_name.replace("-", " ").title()

    skills_dir = Path(__file__).parent.parent.parent / ".agents" / "skills" / skill_name
    skills_dir.mkdir(parents=True, exist_ok=True)
    file_path = skills_dir / "SKILL.md"

    if file_path.exists():
        print(f"❌ Erro: A skill {file_path} já existe.")
        sys.exit(1)

    content = SKILL_TEMPLATE.format(
        skill_name=skill_name,
        description=args.description,
        title=title
    )

    file_path.write_text(content, encoding="utf-8")
    print(f"✅ Skill '{skill_name}' criada com sucesso em: {file_path}")

if __name__ == "__main__":
    main()
