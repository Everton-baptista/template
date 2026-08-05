# Diretrizes do Projeto Template Agno Multi-Agent

Este arquivo define as regras de arquitetura, padrões de engenharia de software e convenções de código que qualquer Agente de IA ou desenvolvedor DEVE seguir ao modificar este repositório.

## 🏗️ Princípios de Arquitetura e Engenharia

1. **Separação Rígida de Camadas (Clean Architecture)**:
   - `backend/app/agents/`: Definições puras de Agentes individuais (ex: `ResearcherAgent`, `CoderAgent`).
   - `backend/app/teams/`: Definições de equipes multiagentes (`agno.team.Team`).
   - `backend/app/workflows/`: Fluxos determinísticos híbridos (`agno.workflow.Workflow`).
   - `backend/app/tools/`: Ferramentas modulares pré-configuradas e customizadas (`Toolkit`).
   - `backend/app/storage/`: Persistência de sessões com `PostgresDb` e `SqliteDb`.
   - `backend/app/api/`: Camada FastAPI exposta nos protocolos **REST JSON**, **SSE Streaming** e **WebSockets**.

2. **Padrões do Agno Framework (Agno 2.x)**:
   - Importar agentes via `from agno.agent import Agent`.
   - Importar equipes via `from agno.team import Team`.
   - Importar storage via `from agno.db.postgres import PostgresDb` e `from agno.db.sqlite import SqliteDb`.
   - Sempre passar `db=get_agent_storage(...)` para os agentes e equipes para garantir persistência.

3. **Protocolos de Comunicação FastAPI**:
   - Todo novo agente ou funcionalidade deve ser exposto e compatível com as rotas REST (`/agent/run`), SSE Streaming (`/agent/stream`) e WebSocket (`/ws/chat`).
   - Manter validação Pydantic v2 estrita em `backend/app/api/schemas.py`.

4. **Frontend Next.js**:
   - Manter UI reativa em TypeScript com Tailwind CSS e componentes modulares sob `frontend/src/components/`.
   - Suportar visualização de logs, carregadores e respostas em tempo real Markdown.

5. **Testabilidade & Qualidade**:
   - Qualquer nova funcionalidade ou agente deve ser acompanhado por testes em `backend/tests/`.
   - Sempre rodar `PYTHONPATH=. .venv/bin/pytest tests/ -v` ou `make test-backend` para validar alterações.
